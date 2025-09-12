<script lang="ts">
	import { goto } from '$app/navigation';
	import { faFileImport } from '@fortawesome/free-solid-svg-icons';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { fileState } from '$stores/selectedFile.svelte';

	const onClick = (e: Event) => {
		const input = e.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;

		fileState.file = file;
		goto('/configure');
	};

	const handleDrop = (event: DragEvent) => {
		event.preventDefault();
		if (!event.dataTransfer?.files.length) return;

		fileState.file = event.dataTransfer.files[0];
		goto('/configure');
	};

	const handleDragOver = (event: DragEvent) => {
		event.preventDefault();
	};
</script>

<div class="drop-container" ondrop={handleDrop} ondragover={handleDragOver} role="region">
	<FontAwesomeIcon icon={faFileImport} size="4x" />
	<div class="header">
		<h2>Drop your audio file here</h2>
		<p>For best results, use a high-quality audio file (WAV or FLAC).</p>
	</div>
	<button class="file-input-button" onclick={() => document.getElementById('audio-file')?.click()}>
		<span>Select File</span>
	</button>
	<input id="audio-file" type="file" accept="audio/*" class="file-input" onchange={onClick} />
</div>

<style lang="scss">
	.header {
		text-align: center;
	}

	.drop-container {
		position: relative;
		border-radius: 0.5rem;
		padding: 6rem 2rem;
		width: 100%;
		max-width: 600px;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		flex-grow: 1;
		justify-content: center;
		align-items: center;
		transition: background-color 0.3s ease;
		border: 2px dashed var(--color-border);
		background-color: var(--color-surface);

		span {
			text-align: center;
		}

		&:hover {
			background-color: var(--color-hover);
		}

		button.file-input-button {
			background-color: var(--color-accent);
			color: var(--color-text);
			border: none;
			padding: 0.5rem 1.5rem;
			border-radius: 20px;
			cursor: pointer;
			transition: background-color 0.3s ease;
		}
	}

	.file-input {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		opacity: 0;
		cursor: pointer;
	}
</style>
