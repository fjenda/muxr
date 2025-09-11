<script lang="ts">
	import { AudioPlayer } from '$components';
	import { DialogActions, type DialogComponent } from '$providers/dialog.svelte';
	import { AlertDialog } from '$dialogs';

	import { page } from '$app/state';
	import { fileState } from '$stores/selectedFile.svelte';
	import { goto } from '$app/navigation';
	const sessionId = page.params.sessionId;

	const showAlert = (file: File) => {
		DialogActions.show(AlertDialog as DialogComponent, {
			title: 'Important notice',
			message: 'Replace the current track? Progress will be lost.',
			onCancel: () => {
				DialogActions.close();
			},
			onConfirm: () => {
				DialogActions.close();
				fileState.file = file;
				fileState.url = null;
				goto('/configure');
			}
		});
	};

	const handleDrop = (event: DragEvent) => {
		event.preventDefault();
		if (!event.dataTransfer?.files.length) return;

		const file = event.dataTransfer.files[0];
		showAlert(file);
	};

	const handleDragOver = (event: DragEvent) => {
		event.preventDefault();
	};
</script>

<div class="container" ondrop={handleDrop} ondragover={handleDragOver} role="region">
	<AudioPlayer barHeight={128} timelineHeight={30} {sessionId} />
</div>

<style>
	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: var(--color-bg);
		border-radius: 0.5rem;
		flex-grow: 1;
		position: relative;
		z-index: 0;
	}

	.container::before {
		content: 'muxr';
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		opacity: 0.1;
		font-size: 12.5rem;
		font-weight: bold;
		color: var(--color-text);
		pointer-events: none;
		user-select: none;
		z-index: -1;
		filter: blur(2px);
	}

	@media screen and (max-width: 650px) {
		.container::before {
			font-size: 8rem;
		}
	}
</style>
