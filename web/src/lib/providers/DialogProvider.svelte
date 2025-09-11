<script lang="ts">
	import { dialogState, DialogActions } from './dialog.svelte';

	let { children } = $props();

	const handleBackdropClick = (e: MouseEvent) => {
		if (e.target === e.currentTarget) {
			DialogActions.close();
		}
	};

	$effect(() => {
		if (dialogState.open) {
			document.body.style.overflow = 'hidden';
		} else {
			document.body.style.overflow = '';
		}
	});
</script>

{@render children()}
{#if dialogState.open}
    <div class="dialog-backdrop" role="region" aria-label="Dialog backdrop">
        <div
            class="backdrop-click-layer"
            onclick={handleBackdropClick}
            aria-hidden="true"
        ></div>

        <div class="dialog-container">
            {#if dialogState.component}
                <dialogState.component
                    {...dialogState.props}
                    close={DialogActions.close}
                />
            {/if}
        </div>
    </div>
{/if}

<style>
	.dialog-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.7);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
		backdrop-filter: blur(3px);
		animation: fade-in 0.3s ease-out;
	}

    .backdrop-click-layer {
        position: absolute;
        inset: 0;
        background: rgba(0, 0, 0, 0.7);
    }

    .dialog-container {
        background: var(--color-surface);
        color: var(--color-text);
        border-radius: 0.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        max-width: 90%;
        max-height: 90vh;
        overflow: auto;
        animation: scale-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

	@keyframes fade-in {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@keyframes scale-in {
		from {
			transform: scale(0.9);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}
</style>
