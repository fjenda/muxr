<script>
    import { LoadingProvider, DialogProvider } from "$providers";
    import { faMoon, faSun, faWaveSquare } from '@fortawesome/free-solid-svg-icons'
    import { faGithub } from "@fortawesome/free-brands-svg-icons";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import { Button } from '$components'
    let { children } = $props();

    let isDarkMode = $state(false);

    // system preference
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
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
                    <li><a href="/">
                        <FontAwesomeIcon icon={faWaveSquare} size="1x"/>
                        muxr
                    </a></li>
                </ul>
                <ul>
                    <li>
                        <a href="https://github.com/fjenda/muxr" target="_blank" rel="noopener noreferrer">
                            <FontAwesomeIcon icon={faGithub} size="1x"/>
                        </a>
                    </li>
                    <li>
                        <Button onClick={toggleDarkMode} style="padding: 0.45rem 0.7rem; font-size: 0.8em;">
                          {#if isDarkMode}
                            <FontAwesomeIcon icon={faSun} size="1x"/>
                          {:else}
                            <FontAwesomeIcon icon={faMoon} size="1x"/>
                          {/if}
                        </Button>
                    </li>
                </ul>
            </nav>
            {@render children()}
        </main>
    </DialogProvider>
</LoadingProvider>


<style>
    .container {
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #0f0f0f;
        padding: .5rem 0;
        font-size: 1.2rem;
        border-bottom: 1px solid #333;
    }
    nav ul {
        list-style: none;
        display: flex;
        align-items: center;
        gap: 1rem;
        /*height: 100%;*/
        margin: 0;
        padding: 0 2rem;
    }
    nav a {
        text-decoration: none;
        color: white;
        font-weight: bold;
    }
    :global(html):not(.dark-mode) {
      nav {
        background: #edeff8;
        border-color: #ccc;
      }
      nav a {
        color: #101220;
      }
    }
</style>