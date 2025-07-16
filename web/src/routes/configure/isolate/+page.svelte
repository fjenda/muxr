<script lang="ts">
    import { Button, Card } from "$components";
    import { goto } from "$app/navigation";
    import { faMicrophone, faDrum, faGuitar, faQuestion, faKeyboard } from "@fortawesome/free-solid-svg-icons";
    import { configurationState, StemType } from "$stores/configuration.svelte";
    import { separate } from "$utils/separate";
    import { processingState } from "$stores/processingState.svelte";
    import { LoadingActions } from "$providers/loading.svelte";

    const options = [
        { icon: faMicrophone, title: "Vocals" },
        { icon: faGuitar, title: "Bass" },
        { icon: faDrum, title: "Drums" },
        { icon: faQuestion, title: "Other" },
        // { icon: faKeyboard, title: "Piano" }, // faPiano is pro only
        // { icon: faGuitar, title: "Guitar" },
    ];

    let selected = "";
    const handleCardClick = (title: string) => selected = title;
    const continueToNext = async () => {
        if (selected) {
            configurationState.pickedStem = selected as StemType;
            await separate();
            if (processingState.status === "Idle") return;
            LoadingActions.show(processingState.status);
        }
    }
</script>

<div class="container">
    <div class="header">
        <h2 class="title">Seperate Your Track</h2>
        <p>muxr will automatically detect the selected option in your audio and split it into a separate track.</p>
    </div>
    <div class="card-grid">
        {#each options as { icon, title }}
            <Card {icon} {title} selected={selected === title} onClick={() => handleCardClick(title)} />
        {/each}
    </div>
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
        grid-template-columns: repeat(4, minmax(250px, 1fr));
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

        .card-grid {
            grid-template-columns: repeat(2, minmax(250px, 1fr));
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
</style>