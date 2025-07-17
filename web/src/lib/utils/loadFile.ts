import { selectedFile } from "$stores/selectedFile.svelte";

export const onDrop = async (file: File) => {
    selectedFile.file = file;
};

export const onFileSelect = (event: Event) => {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    selectedFile.file = file;
};
