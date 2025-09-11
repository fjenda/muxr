<script lang="ts">
	let { onClick, children, ...rest } = $props();
</script>

<button onclick={onClick} {...rest}>
	{@render children()}
</button>

<style lang="scss">
	button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.6em 1.2em;
		font-size: 1em;
		font-weight: 500;
		border-radius: 0.5rem;
		border: 1px solid rgba(200, 200, 200, 0.1);
		background: rgba(255, 255, 255, 0.8);
		//background: var(--color-surface);
		color: var(--color-text);
		backdrop-filter: blur(6px);
		-webkit-backdrop-filter: blur(6px);
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
		transition: all 0.2s ease-in-out;
		cursor: pointer;
		outline: none;

		&:hover,
		&:focus-visible {
			background: rgba(255, 255, 255, 0.5);
			box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
			border-color: rgba(255, 255, 255, 0.2);
		}

		&:active {
			box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
		}

		&:disabled {
			opacity: 0.4;
			cursor: not-allowed;
			pointer-events: none;
			background: rgba(200, 200, 200, 0.1);
			border-color: transparent;
		}

		:global(html.dark-mode) & {
			background: rgba(34, 34, 34, 0.8);
			border: 1px solid rgba(255, 255, 255, 0.1);
			box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);

			&:hover,
			&:focus-visible {
				background: rgba(50, 50, 50, 0.25);
				border-color: rgba(255, 255, 255, 0.2);
			}

			&:disabled {
				background: rgba(60, 60, 60, 0.1);
			}
		}
	}
</style>
