<script lang="ts">
	import { loading } from '$providers/loading.svelte';
</script>

{#if loading.visible}
	<div class="loading-overlay">
		<div class="spinner">
			<div class="spinner-sector"></div>
			<div class="spinner-sector"></div>
			<div class="spinner-sector"></div>
		</div>
		<div class="loading-message">{loading.message}</div>
	</div>
{/if}

<style>
	.loading-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.7);
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		z-index: 9999;
		backdrop-filter: blur(2px);
	}

	.spinner {
		position: relative;
		width: 80px;
		height: 80px;
	}

	.spinner-sector {
		position: absolute;
		width: 100%;
		height: 100%;
		border-radius: 50%;
		border: 8px solid transparent;
		mix-blend-mode: overlay;
	}

	.spinner-sector:nth-child(1) {
		border-top-color: #646cff;
		animation: rotate 1s infinite ease-in-out;
	}

	.spinner-sector:nth-child(2) {
		border-left-color: #00ff99;
		animation: rotate 1.5s infinite ease-in-out;
	}

	.spinner-sector:nth-child(3) {
		border-right-color: #ff66aa;
		animation: rotate 2s infinite ease-in-out;
	}

	.loading-message {
		margin-top: 20px;
		color: white;
		font-size: 1.2rem;
		max-width: 300px;
		text-align: center;
	}

	@keyframes rotate {
		0% {
			transform: rotate(0);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
