<script lang="ts">
	let selectedFile: File | null = null;
	let sessionId: string | null = null;
	let status: string | null = null;

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files.length > 0) {
			selectedFile = input.files[0];
			uploadFile();
		}
	}

	function triggerFileSelect() {
		const input = document.createElement("input");
		input.type = "file";
		input.accept = "audio/*";
		input.onchange = handleFileChange;
		input.click();
	}

	async function uploadFile() {
		if (!selectedFile) return;

		const formData = new FormData();
		formData.append("file", selectedFile);
		formData.append("model", "htdemucs");
		formData.append("mp3", "false");
		formData.append("mp3_bitrate", "320");
		// formData.append("two_stems", "drums");

		status = "Uploading your file...";

		try {
			const res = await fetch("api/separate", {
				method: "POST",
				body: formData
			});
			const data = await res.json();
			sessionId = data.session_id;
			status = "Separating...";
			await pollResult();
		} catch (err) {
			console.error("Upload error:", err);
			status = "Upload failed";
		}
	}

	async function pollResult() {
		if (!sessionId) return;

		let percentage = 0;

		const interval = setInterval(async () => {
			const res = await fetch(`api/result/${sessionId}`);
			if (res.status === 202) {
				try {
					const body = await res.json();
					console.log(body);
					percentage = body.progress?.percentage || percentage;
					status = `Processing (${sessionId}) at ${percentage}%`;
				} catch {}
				return;
			}

			clearInterval(interval);
			if (res.ok) {
				const blob = await res.blob();
				const url = URL.createObjectURL(blob);
				const a = document.createElement("a");
				a.href = url;
				a.download = `stems_${sessionId}.zip`;
				document.body.appendChild(a);
				a.click();
				document.body.removeChild(a);
				URL.revokeObjectURL(url);
				status = "Download started";
			} else {
				const errData = await res.json();
				status = `Error: ${errData.message}`;
			}
		}, 2000);
	}
</script>

<button on:click={triggerFileSelect}>
	Select Song
</button>

{#if status}
	<p>{status}</p>
{/if}
