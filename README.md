# muxr

A web app for splitting music tracks into stems (vocals, drums, etc.) using [Demucs](https://github.com/facebookresearch/demucs).
It splits your track and displays the result in a timeline with audio waveforms and useful playback controls.

### Features
- Svelte frontend with waveform visualization
- FastAPI backend with multithreaded stem processing
- Supports MP3, WAV, and FLAC export
- Concurrent job handling with timeouts
- Docker-friendly and lightweight

---

### Requirements
- python 3.11
- `ffmpeg` installed and in `PATH`
- docker (optional, for containerized deployment)

---

### Installation

```bash
git clone https://github.com/fjenda/muxr.git
cd muxr
# create a virtual environment
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# install frontend dependencies
cd web
npm install
```

### Running the App

```bash
# start the FastAPI backend
cd api
python3 main.py
# start the svelte client
cd web
npm run dev
```
### Docker Deployment
You can simply run the app using Docker Compose. This will build the Docker images and start the services.
```bash
docker-compose up --build
```
