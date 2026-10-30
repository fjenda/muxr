import { fileState } from '$stores/selectedFile.svelte';
import { configurationState, FileType } from '$stores/configuration.svelte';
import { processingState } from '$stores/processingState.svelte';
import { LoadingActions } from '$providers/loading.svelte';
import { unzipSync } from 'fflate';
import { getMimeType } from '$utils/mimetype';
import { trackUrls } from '$stores/trackUrls.svelte.js';
import { goto } from '$app/navigation';
import { DialogActions, type DialogComponent } from '$providers/dialog.svelte';
import { AlertDialog } from '$dialogs';

const showError = (message: string) => {
	LoadingActions.hide();
	document.title = 'muxr';
	DialogActions.show(AlertDialog as DialogComponent, {
		title: 'Processing failed',
		message,
		onConfirm: () => DialogActions.close(),
		onCancel: () => DialogActions.close()
	});
};

const readErrorMessage = async (res: Response, fallback: string) => {
	try {
		const body = await res.json();
		return body?.message || fallback;
	} catch {
		return fallback;
	}
};

export const separate = async (youtube_url: string | null) => {
	if (fileState.file === null && !youtube_url) {
		console.error('No file selected for separation.');
		return goto('/');
	}

	const formData = new FormData();
	if (fileState.file) {
		formData.append('file', fileState.file);
	} else if (youtube_url) {
		formData.append('url', youtube_url);
	}
	formData.append('model', 'htdemucs');
	formData.append('output_format', configurationState.outputFileType as string);

	if (configurationState.outputFileType === FileType.MP3) formData.append('mp3_bitrate', '320');

	if (configurationState.twoStems) {
		formData.append('two_stems', (configurationState.pickedStem as string).toLowerCase());
	}

	console.log('Starting separation with form data:');
	Array.from(formData.keys()).forEach((key: string) => {
		console.log(`${key}: ${formData.get(key)}`);
	});

	processingState.status = youtube_url ? 'Downloading YouTube audio...' : 'Uploading file...';
	LoadingActions.show(processingState.status);

	try {
		const res = await fetch('/api/separate', {
			method: 'POST',
			body: formData
		});
		if (!res.ok) {
			const message = await readErrorMessage(res, `Upload failed (${res.status})`);
			processingState.status = `Error: ${message}`;
			await goto('/');
			return showError(message);
		}
		const data = await res.json();
		processingState.sessionId = data.session_id;
		processingState.status = youtube_url ? 'Downloading YouTube audio...' : 'Separating...';
		await pollResult();
	} catch (err) {
		console.error('Upload error:', err);
		processingState.status = 'Upload failed';
		await goto('/');
		showError('Upload failed. Is the server running?');
	}
};

export const pollResult = async (sessionId?: string) => {
	if (sessionId) processingState.sessionId = sessionId;

	if (!processingState.sessionId) {
		console.error('No session ID provided for polling.');
		return;
	}

	processingState.percentage = 0;

	let busy = false;
	const interval = setInterval(async () => {
		// skip ticks while a previous request is still in flight
		if (busy) return;
		busy = true;
		try {
			await pollOnce(interval);
		} catch (err) {
			console.error('Polling error:', err);
		} finally {
			busy = false;
		}
	}, 2000);
};

const pollOnce = async (interval: ReturnType<typeof setInterval>) => {
	LoadingActions.show(processingState.status);
	const res = await fetch(`/api/result/${processingState.sessionId}`);
	if (res.status === 202) {
		try {
			const body = await res.json();
			console.log(body);
			const progress = body.progress ?? {};
			if (progress.type === 'info' && progress.message && !progress.percentage) {
				processingState.status = `${progress.message}...`;
			} else {
				processingState.percentage = progress.percentage || processingState.percentage;
				processingState.status = `Processing (${processingState.sessionId}) at ${processingState.percentage}%`;
			}
			document.title = `${processingState.percentage}% ${
				fileState.file?.name ? `- ${fileState.file.name} |` : ''
			} muxr`;
		} catch {
			/* empty */
		}
		return;
	}

	clearInterval(interval);
	if (res.status === 404) {
		console.error('Session not found, redirecting to home.');
		LoadingActions.hide();
		await goto('/');
		document.title = 'muxr';
		return;
	}

	if (!res.ok) {
		const message = await readErrorMessage(res, 'Separation failed.');
		processingState.status = `Error: ${message}`;
		await goto('/');
		showError(message);
		return;
	}

	const blob = await res.blob();
	const url = URL.createObjectURL(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = `stems_${processingState.sessionId}.zip`;
	trackUrls.downloadZip = () => {
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
	};
	await decompressZipBlob(blob);
	LoadingActions.hide();
	document.title = `${fileState.file?.name ? `${fileState.file.name} |` : ''} muxr`;
	await goto(`/${processingState.sessionId}`);
};

async function decompressZipBlob(blob: Blob) {
	try {
		const arrayBuffer = await blob.arrayBuffer();
		const uint8Array = new Uint8Array(arrayBuffer);

		const extracted = unzipSync(uint8Array); // returns { [filename: string]: Uint8Array }

		trackUrls.clear(); // clear previous URLs
		for (const [filename, data] of Object.entries(extracted)) {
			const title = filename.split('.').slice(0, -1).join('.');
			const type = getMimeType(filename);

			const arrayBuffer = new Uint8Array(data).buffer;
			const fileBlob = new Blob([arrayBuffer], { type });
			const url = URL.createObjectURL(fileBlob);

			trackUrls.addUrl({ title, url });
		}

		processingState.status = 'Decompression and processing complete';
	} catch (err) {
		console.error('Decompression error:', err);
		processingState.status = 'Decompression failed';
	}
}
