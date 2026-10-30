import json

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import shutil
import subprocess
import zipfile
import os
import argparse
import sys

# for watching dead clients
import threading
import time
from datetime import datetime, timezone

from yt_dlp import YoutubeDL

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.resolve()
UPLOAD_ROOT = BASE_DIR / "uploads"
OUTPUT_ROOT = BASE_DIR / "outputs"
UPLOAD_ROOT.mkdir(exist_ok=True)
OUTPUT_ROOT.mkdir(exist_ok=True)

MODELS = {"htdemucs", "htdemucs_ft", "htdemucs_6s", "hdemucs_mmi", "mdx", "mdx_extra", "mdx_q", "mdx_extra_q"}
OUTPUT_FORMATS = {"mp3", "wav", "flac"}
STEMS = {"vocals", "drums", "bass", "other"}
STEMS_6S = STEMS | {"guitar", "piano"}

def write_status(output_path: Path, success: bool, message: str = ""):
    if message:
        (output_path / "error.txt").write_text(message)
    (output_path / "status.txt").write_text("success" if success else "error")

def convert_to_wav(src: Path, dst: Path):
    # normalize whatever ffmpeg can decode (any codec/container, video files, mono, surround,
    # odd sample rates) into the 44.1kHz stereo PCM that demucs expects
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src),
        "-map", "0:a:0", "-vn", "-sn", "-dn",
        "-ac", "2", "-ar", "44100", "-c:a", "pcm_s16le",
        str(dst),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not dst.exists() or dst.stat().st_size == 0:
        detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "unknown error"
        if "matches no streams" in result.stderr:
            detail = "file contains no audio stream"
        raise RuntimeError(f"could not decode audio: {detail}")

def parse_human_size(size_str) -> float:
    units = {'K': 1e3, 'M': 1e6, 'G': 1e9}
    try:
        if size_str[-1] in units:
            return float(size_str[:-1]) * units[size_str[-1]]
        return float(size_str)
    except ValueError:
        return 0.0

def run_demucs(file_path: Path, output_path: Path, model: str, output_format: str, mp3_bitrate: int, two_stems: str | None):
    cmd = [
        sys.executable, "-m", "demucs.separate",
        "-n", model,
        "-j", str(max(1, (os.cpu_count() or 2) // 2)),
        "-o", str(output_path),
    ]

    match output_format:
        case "mp3":
            cmd.append("--mp3")
            cmd.append(f"--mp3-bitrate={mp3_bitrate}")
        case "flac":
            cmd.append("--flac")
        case _:
            pass

    if two_stems:
        cmd.append(f"--two-stems={two_stems}")
    cmd.append(str(file_path))

    progress_file = output_path / "progress.json"
    progress_file.write_text(json.dumps({"type": "start", "percentage": 0}))

    poll_file = output_path / "last_poll.txt"
    poll_file.write_text(datetime.now(timezone.utc).isoformat())

    print(cmd)

    process = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
    log_lines = []

    def poll_watcher(proc):
        while proc.poll() is None:
            try:
                last_poll = datetime.fromisoformat(poll_file.read_text())
                delta = (datetime.now(timezone.utc) - last_poll).total_seconds()
                if delta > 15:
                    proc.kill()
                    print(f"[{file_path.name}] Poll timeout, killed process")
                    return
            except Exception:
                pass
            time.sleep(1)

    threading.Thread(target=poll_watcher, args=(process,), daemon=True).start()

    for line in process.stdout:
        line = line.strip()
        if not line:
            continue
        log_lines.append(line)
        # print(line)
        if "%" in line and "|" in line and "/" in line:
            try:
                percent_str = line.split('%')[0].strip()
                percentage = float(percent_str)

                fraction_part = [part for part in line.split() if "/" in part]
                if fraction_part:
                    current, total = fraction_part[0].split('/')
                    current = parse_human_size(current)
                    total = parse_human_size(total)
                    progress_file.write_text(json.dumps({
                        "type": "progress",
                        "percentage": percentage,
                        "current": current,
                        "total": total,
                    }))
                    continue
            except Exception as e:
                print(f"Error parsing progress line: {line}, error: {e}")
                pass

        # fallback info
        progress_file.write_text(json.dumps({"type": "info", "message": line}))

    process.wait()
    (output_path / "log.txt").write_text("\n".join(log_lines))

    if process.returncode != 0:
        tail = next((l for l in reversed(log_lines) if "Error" in l), log_lines[-1] if log_lines else "")
        raise RuntimeError(f"separation failed: {tail}" if tail else "separation failed")

    stems_dir = output_path / model / file_path.stem
    stem_files = sorted(stems_dir.glob("*")) if stems_dir.exists() else []
    if not stem_files:
        raise RuntimeError("separation produced no output")

    # write to a temp name first so the poller never serves a half-written zip
    tmp_zip = output_path / "result.zip.part"
    with zipfile.ZipFile(tmp_zip, "w") as zipf:
        for stem_file in stem_files:
            zipf.write(stem_file, arcname=stem_file.name)
    tmp_zip.rename(output_path / "result.zip")


def process_job(source: Path | None, url: str | None, output_path: Path, model: str, output_format: str,
                mp3_bitrate: int, two_stems: str | None):
    progress_file = output_path / "progress.json"
    try:
        if url:
            progress_file.write_text(json.dumps({"type": "info", "message": "Downloading audio"}))
            source = download_youtube_audio(url, output_path / "download")

        progress_file.write_text(json.dumps({"type": "info", "message": "Decoding audio"}))
        wav_path = output_path / "input.wav"
        convert_to_wav(source, wav_path)

        run_demucs(wav_path, output_path, model, output_format, mp3_bitrate, two_stems)
        write_status(output_path, True)
    except Exception as e:
        print(f"[{output_path.name}] job failed: {e}")
        write_status(output_path, False, str(e))
    finally:
        # drop intermediates, keep only the results
        if source and source.exists() and UPLOAD_ROOT in source.parents:
            source.unlink(missing_ok=True)
        shutil.rmtree(output_path / "download", ignore_errors=True)
        (output_path / "input.wav").unlink(missing_ok=True)


@app.post("/separate")
async def separate_audio(
        background_tasks: BackgroundTasks,
        file: UploadFile | None = File(None),
        url: str | None = Form(None),
        model: str = Form("htdemucs"),
        output_format: str = Form("mp3"),
        mp3_bitrate: int = Form(320),
        two_stems: str | None = Form(None)
):
    url = url.strip() if url else None
    if not file and not url:
        return JSONResponse(status_code=400, content={"status": "error", "message": "No file or URL provided."})
    if model not in MODELS:
        return JSONResponse(status_code=400, content={"status": "error", "message": f"Unknown model: {model}"})
    if output_format not in OUTPUT_FORMATS:
        return JSONResponse(status_code=400, content={"status": "error", "message": f"Unsupported output format: {output_format}"})
    two_stems = two_stems.strip().lower() if two_stems and two_stems.strip() else None
    if two_stems and two_stems not in (STEMS_6S if model == "htdemucs_6s" else STEMS):
        return JSONResponse(status_code=400, content={"status": "error", "message": f"Unsupported stem: {two_stems}"})

    session_id = str(uuid.uuid4())
    output_path = OUTPUT_ROOT / session_id
    output_path.mkdir(exist_ok=True)
    # the poll watcher only starts once demucs runs; seed the poll file for the download/decode phase
    (output_path / "last_poll.txt").write_text(datetime.now(timezone.utc).isoformat())
    (output_path / "progress.json").write_text(json.dumps({"type": "start", "percentage": 0}))

    file_path = None
    if file:
        # never trust the client filename for paths, only keep a sane extension
        suffix = Path(file.filename or "").suffix.lower()
        if not suffix.isascii() or not suffix[1:].isalnum():
            suffix = ""
        file_path = UPLOAD_ROOT / f"{session_id}{suffix}"
        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)
        url = None

    background_tasks.add_task(process_job, file_path, url, output_path, model, output_format, mp3_bitrate, two_stems)

    return JSONResponse(
        status_code=202,
        content={"session_id": session_id, "status": "processing"}
    )

@app.get("/result/{session_id}")
def get_result(session_id: str):
    output_path = OUTPUT_ROOT / session_id
    status_file = output_path / "status.txt"
    zip_file = output_path / "result.zip"
    progress_file = output_path / "progress.json"
    poll_file = output_path / "last_poll.txt"

    if not output_path.exists():
        return JSONResponse(
            status_code=404,
            content={"status": "not_found", "message": f"Session ID {session_id} does not exist."}
        )

    poll_file.write_text(datetime.now(timezone.utc).isoformat())

    if not status_file.exists():
        progress = {}
        if progress_file.exists():
            try:
                progress = json.loads(progress_file.read_text())
            except Exception:
                progress = {"type": "unknown"}
        return JSONResponse(status_code=202, content={"status": "processing", "progress": progress})

    # we're done, send the zipfile
    status = status_file.read_text().strip()
    if status == "success" and zip_file.exists() and zip_file.stat().st_size > 0:
        return FileResponse(
            zip_file,
            media_type="application/zip",
            filename=f"stems_{session_id}.zip"
        )
    else:
        error_file = output_path / "error.txt"
        message = error_file.read_text() if error_file.exists() else "Separation failed."
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": message}
        )

def download_youtube_audio(url: str, download_dir: Path) -> Path:
    download_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        # prefer audio-only streams, fall back to a muxed stream; audio is extracted by convert_to_wav
        'format': 'bestaudio/best',
        'outtmpl': str(download_dir / "%(id)s.%(ext)s"),
        'restrictfilenames': True,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'retries': 5,
        'fragment_retries': 5,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info.get("_type") == "playlist":
                entries = [e for e in info.get("entries") or [] if e]
                if not entries:
                    raise RuntimeError("playlist is empty")
                info = entries[0]
            downloads = info.get("requested_downloads") or []
            downloaded_path = Path(downloads[0]["filepath"]) if downloads else Path(ydl.prepare_filename(info))
    except Exception as e:
        raise RuntimeError(f"failed to download audio: {e}") from e

    if not downloaded_path.exists():
        raise RuntimeError("failed to download audio: downloaded file not found")
    print(f"yt-dlp downloaded to {downloaded_path}")
    return downloaded_path

if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)))
    args = parser.parse_args()

    uvicorn.run("main:app", host="0.0.0.0", port=args.port)
