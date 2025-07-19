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
            await goto(`/${processingState.sessionId}`);
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

<style lang="scss">
    @import '../../../lib/styles/configure';
</style>