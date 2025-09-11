<script>
	import { LoadingProvider, DialogProvider } from '$providers';
	import { faLightbulb, faMoon, faSun, faWaveSquare } from '@fortawesome/free-solid-svg-icons';
	import { faGithub } from '@fortawesome/free-brands-svg-icons';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { Button } from '$components';
	let { children } = $props();

	let isDarkMode = $state(false);

	// system preference
	const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
	isDarkMode = prefersDarkScheme.matches;
	updateDarkModeClass();

	prefersDarkScheme.addEventListener('change', (e) => {
		isDarkMode = e.matches;
		updateDarkModeClass();
	});

	function toggleDarkMode() {
		isDarkMode = !isDarkMode;
		updateDarkModeClass();
	}

	function updateDarkModeClass() {
		document.documentElement.classList.toggle('dark-mode', isDarkMode);
	}
</script>

<LoadingProvider>
	<DialogProvider>
		<main class="container">
			<nav>
				<ul>
					<li>
						<a href="/">
							<FontAwesomeIcon icon={faWaveSquare} size="1x" />
							muxr
						</a>
					</li>
				</ul>
				<ul>
					<li>
						<a
							href="https://github.com/fjenda/muxr"
							target="_blank"
							rel="noopener noreferrer"
							class="github-link"
						>
							<FontAwesomeIcon icon={faGithub} size="1x" />
						</a>
					</li>
					<li>
						<Button
							onClick={toggleDarkMode}
							class="theme-toggle"
							style="padding: 0; border: none; background: none; box-shadow: none"
						>
							{#if isDarkMode}
								<FontAwesomeIcon icon={faSun} size="1x" class="theme-icon" />
							{:else}
								<FontAwesomeIcon icon={faMoon} size="1x" class="theme-icon" />
							{/if}
						</Button>
					</li>
				</ul>
			</nav>
			{@render children()}
		</main>
	</DialogProvider>
</LoadingProvider>

<style lang="scss">
	.container {
		height: 100%;
		display: flex;
		flex-direction: column;
	}
	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		background: var(--color-surface);
		padding: 0.5rem 0;
		font-size: 1.2rem;
		border-bottom: 1px solid var(--color-border);

		ul {
			list-style: none;
			display: flex;
			/*align-items: center;*/
			gap: 1rem;
			margin: 0;
			padding: 0 1rem;

			li {
				display: flex;
				align-items: center;
			}
		}

		a {
			text-decoration: none;
			color: var(--color-text);
			font-weight: bold;
		}
	}

	:global(.github-link svg),
	:global(.theme-icon) {
		display: block;
		height: 1.5rem !important; /* solid icon height */
		width: 1.5rem !important; /* match width for square icons */
	}
</style>
