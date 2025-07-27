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
        "-j", str(os.cpu_count() // 2 or 4),
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

    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

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

    for line in process.stderr:
        line = line.strip()
        if not line:
            continue
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
    success = process.returncode == 0

    (output_path / "status.txt").write_text("success" if success else "error")
    (output_path / "log.txt").write_text(process.stdout.read() + process.stderr.read())

    if success:
        stems_dir = output_path / model / file_path.stem
        if stems_dir.exists():
            zip_path = output_path / "result.zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for stem_file in stems_dir.glob("*"):
                    zipf.write(stem_file, arcname=stem_file.name)


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
    session_id = str(uuid.uuid4())
    file_name = file.filename if file else url.split("?v=")[-1]
    file_path = UPLOAD_ROOT / f"{session_id}_{file_name}"
    output_path = OUTPUT_ROOT / session_id
    output_path.mkdir(exist_ok=True)

    if url:
        try:
            file_path = await download_youtube_audio(url, file_path)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": str(e)}
            )
    else:
        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

    # def run_demucs(file_path: Path, output_path: Path, model: str, output_format: str, mp3_rate: int,
    #                two_stems: str | None):
    background_tasks.add_task(run_demucs, file_path, output_path, model, output_format, mp3_bitrate, two_stems)

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
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Separation failed."}
        )

async def download_youtube_audio(url: str, output_path: Path) -> Path:
    output_template = str(output_path.with_suffix(""))

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
            print(f"yt-dlp downloaded to {downloaded_path}")
            return downloaded_path
    except Exception as e:
        raise RuntimeError(f"failed to download audio from YouTube: {str(e)}") from e


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)))
    args = parser.parse_args()

    uvicorn.run("main:app", host="0.0.0.0", port=args.port)
