<script lang="ts">
    import { goto } from "$app/navigation";
    import { faDrum, faGuitar, faMicrophone } from "@fortawesome/free-solid-svg-icons";
    import { Button, Card } from "$components";
    import { configurationState } from "$stores/configuration.svelte";
    import { separate } from "$utils/separate";
    import { processingState } from "$stores/processingState.svelte";
    import { LoadingActions } from "$providers/loading.svelte";

    const options = [
        { icon: faMicrophone, title: "Isolate one stem" },
        { icon: faDrum, title: "Split the song into all audible stems" },
    ];

    let selected = "";
    // let loading = false
    const handleCardClick = (title: string) => selected = title;
    const continueToNext = async () => {
        if (selected === "Isolate one stem") {
            configurationState.twoStems = true;
            return goto("/configure/isolate");
        }

        await separate();
        if (processingState.status === "Idle") return;
        LoadingActions.show(processingState.status);
        await goto(`/${processingState.sessionId}`);
    };
</script>


<div class="container">
    <div class="header">
        <h2 class="title">Separation type</h2>
    </div>
    <div class="card-grid">
        {#each options as { icon, title }}
            <Card {icon} {title} selected={selected === title} onClick={() => handleCardClick(title)} />
        {/each}
    </div>
    <div id="format-options" role="radiogroup" aria-label="Output format">
        <button type="button" data-format="mp3" class="format-btn selected">MP3</button>
        <button type="button" data-format="wav" class="format-btn">WAV</button>
        <button type="button" data-format="flac" class="format-btn">FLAC</button>
    </div>
    <input type="hidden" name="format" id="format" value="mp3">

    <div class="button-container">
        <Button onClick={continueToNext} tabindex="0" disabled={!selected}>
            Continue
        </Button>
    </div>
</div>

<style>
    .header {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(250px, 1fr));
        max-width: 1200px;
        margin: 0 auto;
        gap: 1rem;
        padding: 1rem;
    }

    .title {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 1rem;
        color: var(--text-color-light);
    }

    .container {
        display: flex;
        flex-direction: column;
        padding: 2rem;
        justify-content: center;
        background-color: var(--accent-color-light);
        border: 2px solid var(--border-color-light);
        border-radius: 0.5rem;
        flex-grow: 1;
        position: relative;
        z-index: 0;
    }

    .container::before {
        content: "muxr";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        opacity: 0.1;
        font-size: 12.5rem;
        font-weight: bold;
        color: var(--text-color-light);
        pointer-events: none;
        user-select: none;
        z-index: -1;
        filter: blur(2px);
    }

    @media screen and (max-width: 1200px) {
        .container {
            padding: 1rem;
        }

        .title {
            font-size: 1.5rem;
        }
    }

    @media screen and (max-width: 650px) {
        .container::before {
            font-size: 8rem;
        }

        .card-grid {
            display: grid;
            gap: 0.5rem;
            padding: 0.5rem;
            grid-template-columns: repeat(1, minmax(250px, 1fr));
        }
    }

    @media screen and (prefers-color-scheme: dark) {
        .title {
            color: var(--text-color-dark);
        }

        .container {
            background-color: var(--element-color-dark);
            border: 2px solid var(--border-color-dark);
        }

        .container::before {
            color: var(--text-color-dark);
        }
    }

    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }

    #format-options {
        display: flex;
        gap: 0.5rem;
    }

    .format-btn {
        padding: 0.5rem 1rem;
        border: 1px solid #ccc;
        background: #f8f8f8;
        cursor: pointer;
        border-radius: 4px;
        font-weight: bold;
        transition: all 0.2s ease;
    }

    .format-btn:hover {
        background: #eaeaea;
    }

    .format-btn.selected {
        background: #007bff;
        color: white;
        border-color: #007bff;
    }

</style>