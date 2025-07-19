import { selectedFile } from '$stores/selectedFile.svelte'
import { configurationState, FileType } from '$stores/configuration.svelte'
import { processingState } from '$stores/processingState.svelte'
import { LoadingActions } from '$providers/loading.svelte'
import { unzipSync } from 'fflate'
import { getMimeType } from '$utils/mimetype'
import { trackUrls } from '$stores/trackUrls.svelte.js'
import { goto } from '$app/navigation'

export const separate = async () => {
  if (!selectedFile.file) {
    console.error("No file selected for separation.");
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.file);
  formData.append("model", "htdemucs");
  formData.append("output_format", configurationState.outputFileType as string);

  if (configurationState.outputFileType === FileType.MP3)
    formData.append("mp3_bitrate", "320");

  if (configurationState.twoStems) {
    formData.append(
      "two_stems",
      (configurationState.pickedStem as string).toLowerCase()
    );
  }

  console.log("Starting separation with form data:");
  Array.from(formData.keys()).forEach((key: string) => {
    console.log(`${key}: ${formData.get(key)}`);
  });

  processingState.status = "Uploading your file...";
  try {
    const res = await fetch("/api/separate", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    processingState.sessionId = data.session_id;
    processingState.status = "Separating...";
    await pollResult();
  } catch (err) {
    console.error("Upload error:", err);
    processingState.status = "Upload failed";
  }
};

export const pollResult = async (sessionId?: string) => {
  if (sessionId) processingState.sessionId = sessionId;

  if (!processingState.sessionId) {
    console.error("No session ID provided for polling.");
    return;
  }

  processingState.percentage = 0;

  const interval = setInterval(async () => {
    LoadingActions.show(processingState.status);
    const res = await fetch(`api/result/${processingState.sessionId}`);
    if (res.status === 202) {
      try {
        const body = await res.json();
        console.log(body);
        processingState.percentage =
          body.progress?.percentage || processingState.percentage;
        processingState.status = `Processing (${processingState.sessionId}) at ${processingState.percentage}%`;
      } catch { /* empty */ }
      return;
    }

    LoadingActions.show(processingState.status);
    clearInterval(interval);
    if (res.status === 404 || res.status === 500) {
      console.error("Session not found, redirecting to home.");
      LoadingActions.hide();
      goto("/");
      return;
    }

    if (res.ok) {
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `stems_${processingState.sessionId}.zip`;
      document.body.appendChild(a);
      trackUrls.downloadZip = () => a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      processingState.status = "Download started";
      await decompressZipBlob(blob);
      LoadingActions.hide();
    } else {
      const errData = await res.json();
      processingState.status = `Error: ${errData.message}`;
    }
  }, 2000);
};

async function decompressZipBlob(blob: Blob) {
  try {
    const arrayBuffer = await blob.arrayBuffer();
    const uint8Array = new Uint8Array(arrayBuffer);

    const extracted = unzipSync(uint8Array); // returns { [filename: string]: Uint8Array }

    trackUrls.clear(); // clear previous URLs
    for (const [filename, data] of Object.entries(extracted)) {
      const title = filename.split(".").slice(0, -1).join("."); // remove extension
      const type = getMimeType(filename);
      const fileBlob = new Blob([data], { type });
      const url = URL.createObjectURL(fileBlob);
      trackUrls.addUrl({ title, url });
    }

    processingState.status = "Decompression and processing complete";
  } catch (err) {
    console.error("Decompression error:", err);
    processingState.status = "Decompression failed";
  }
}
