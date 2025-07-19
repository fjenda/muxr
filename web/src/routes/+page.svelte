<script lang="ts">
  import { DropContainer } from "$components";
</script>

<div class="center">
    <div class="main-container">
        <span>
            <h1 class="title">Separate your audio tracks into stems</h1>
            <p class="subtitle">Upload a song and get the stems in seconds</p>
        </span>
        <DropContainer />
    </div>
</div>

<style lang="scss">
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .main-container {
        padding: 4rem 2rem;
        display: flex;
        gap: 2rem;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .title {
        text-align: center;
        color: var(--text-color-light);
        font-size: 2.5rem;
    }

    .subtitle {
        text-align: center;
        color: var(--text-color-light);
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

    @media screen and (prefers-color-scheme: dark) {
        .title {
            color: var(--text-color-dark);
        }

        .subtitle {
            color: var(--text-color-dark);
        }
    }
</style>

