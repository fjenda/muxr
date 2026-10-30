FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

# yt-dlp needs a JS runtime to download from YouTube
COPY --from=denoland/deno:bin /deno /usr/local/bin/deno

# the container has no GPU access, so use the CPU-only torch wheels instead of the multi-GB CUDA ones
ENV PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
