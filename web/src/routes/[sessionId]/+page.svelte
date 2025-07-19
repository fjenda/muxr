<script lang="ts">
    import { AudioPlayer } from "$components";
    import { DialogActions, type DialogComponent } from "$providers/dialog.svelte";
    import { AlertDialog } from "$dialogs";
    import { onDrop } from "$utils/loadFile";

    import { page } from '$app/state';
    const sessionId = page.params.sessionId;

    const showAlert = (file: File) => {
        DialogActions.show(AlertDialog as DialogComponent, {
            title: "Important notice",
            message: "Replace the current track? Progress will be lost.",
            onCancel: () => {
                DialogActions.close();
            },
            onConfirm: async () => {
                DialogActions.close();
                await onDrop(file);
            }
        });
    };

    const handleDrop = async (event: DragEvent) => {
        event.preventDefault();
        if (!event.dataTransfer?.files.length) return;

        const file = event.dataTransfer.files[0];
        showAlert(file);
    }

    const handleDragOver = (event: DragEvent) => {
        event.preventDefault();
    }
</script>

<div class="container"
     ondrop={handleDrop}
     ondragover={handleDragOver}
     role="region"
>
    <AudioPlayer barHeight={128} timelineHeight={30} sessionId={sessionId} />
</div>

<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
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

    @media screen and (max-width: 650px) {
        .container::before {
            font-size: 8rem;
        }
    }

    @media screen and (prefers-color-scheme: dark) {
        .container {
            background-color: var(--element-color-dark);
            border: 2px solid var(--border-color-dark);
        }

        .container::before {
            color: var(--text-color-dark);
        }
    }
</style>