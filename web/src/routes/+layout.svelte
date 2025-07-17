<script>
    import { LoadingProvider, DialogProvider } from "$providers";
    import { faWaveSquare } from "@fortawesome/free-solid-svg-icons";
    import { faGithub } from "@fortawesome/free-brands-svg-icons";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    let { children } = $props();
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
    }
    nav ul {
        list-style: none;
        display: flex;
        gap: 1rem;
        color: white;
        margin: 0;
        padding: 0 2rem;
    }
    nav a {
        text-decoration: none;
        color: white;
        font-weight: bold;
    }
</style>