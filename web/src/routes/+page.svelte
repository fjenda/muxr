<script lang="ts">
	import { DropContainer } from '$components';
	import UrlContainer from '$components/UrlContainer.svelte';

	document.title = 'muxr';
</script>

<div class="center">
	<div class="main-container">
		<div class="header">
			<h1 class="title">Separate your audio tracks into stems</h1>
			<p class="subtitle">Upload a song and get the stems in seconds</p>
		</div>
		<div class="containers">
			<DropContainer />
			<UrlContainer />
		</div>
	</div>
</div>

<style lang="scss">
	.header {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: 0; // prevent collapsed margins
		padding-top: 1rem;
	}

	.center {
		display: flex;
		justify-content: center;
		//align-items: center;
		height: 100%;
	}

	.main-container {
		padding: 4rem 2rem;
		display: flex;
		gap: 2rem;
		flex-direction: column;
		justify-content: flex-start;
		align-items: stretch;
		width: 100%;
		height: fit-content;
	}

	.containers {
		display: flex;
		flex-direction: row;
		gap: 2rem;
		width: 100%;
		height: auto;
		justify-content: center;
	}

	.title {
		text-align: center;
		color: var(--color-text);
		font-size: 2.5rem;
	}

	.subtitle {
		text-align: center;
		color: var(--color-text);
		font-size: 1.5rem;
	}

	@media screen and (max-width: 600px) {
		.main-container {
			padding: 2rem 1rem;
		}

		.title {
			font-size: 1.8rem;
		}

		.subtitle {
			font-size: 1.2rem;
		}
	}

	@media screen and (max-width: 900px) {
		.containers {
			flex-direction: column;
			align-items: center;
		}
	}
</style>
