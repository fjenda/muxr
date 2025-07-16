<script lang="ts">
    import { onDrop, onFileSelect } from "$utils/loadFile";
    import { goto } from "$app/navigation";

    const onClick = (e: Event) => {
        onFileSelect(e);
        goto('/configure');
    }

    const handleDrop = async (event: DragEvent) => {
        event.preventDefault();
        if (!event.dataTransfer?.files.length) return;

        const file = event.dataTransfer.files[0];
        await onDrop(file);
        await goto('/configure');
    }

    const handleDragOver = (event: DragEvent) => {
        event.preventDefault();
    }
</script>

<div class="drop-container" ondrop={handleDrop} ondragover={handleDragOver}>
    <h2>Drop your track here.</h2>
    <input
            id="audio-file"
            type="file"
            accept="audio/*"
            class="file-input"
            onchange={onClick}
    />
</div>

<style>
    .drop-container {
        position: relative;
        border-radius: 0.5rem;
        padding: 1rem;
        width: 100%;
        display: flex;
        flex-grow: 1;
        justify-content: center;
        align-items: center;
        transition: background-color 0.3s ease;
        border: 2px dashed var(--border-color-light);
        background-color: var(--element-color-light);
    }

    .file-input {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: pointer;
    }

    .drop-container:hover {
        background-color: #eaeaea;
    }

    @media screen and (prefers-color-scheme: dark) {
        .drop-container {
            border: 2px dashed var(--border-color-dark);
            background-color: var(--element-color-dark);
        }

        .drop-container:hover {
            background-color: #181818;
        }
    }
</style>