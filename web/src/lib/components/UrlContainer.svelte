<script lang="ts">
	import { goto } from '$app/navigation';
	import { faLink } from '@fortawesome/free-solid-svg-icons';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { fileState } from '$stores/selectedFile.svelte';

	let youtubeUrl = '';

	const handleSubmit = () => {
		if (!youtubeUrl.trim()) return;
		fileState.url = youtubeUrl.trim();
		fileState.file = null;
		goto('/configure');
	};
</script>

<div class="url-container">
	<FontAwesomeIcon icon={faLink} size="4x" />
	<div class="header">
		<h2>Paste a YouTube URL</h2>
		<p>We'll download and process it for you.</p>
	</div>
	<input
		type="text"
		bind:value={youtubeUrl}
		placeholder="https://www.youtube.com/watch?v=..."
		class="url-input"
		on:keydown={(e) => {
			if (e.key === 'Enter') {
				handleSubmit();
			}
		}}
	/>
	<button class="submit-button" on:click={handleSubmit}> Use this link </button>
</div>

<style lang="scss">
	.header {
		text-align: center;
	}

	.url-container {
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
		border: 1px solid var(--color-border);
		background-color: var(--color-surface);
		text-align: center;

		.url-input {
			width: 100%;
			max-width: 400px;
			padding: 0.5rem 1rem;
			font-size: 1rem;
			border-radius: 20px;
			border: 1px solid #ccc;
		}

		.submit-button {
			background-color: var(--color-accent);
			color: var(--color-text);
			border: none;
			padding: 0.5rem 1.5rem;
			border-radius: 20px;
			cursor: pointer;
		}
	}
</style>
