import { getMimeType } from "$lib/utils/mimetype";
import { LoadingActions } from "$providers/loading.svelte";
import { fileState, selectedFile, setSelectedFile } from "$stores/selectedFile.svelte";
import { goto } from "$app/navigation";

const loadFile = async (file: File)
    : Promise<Promise<{ fileName: string, url: string }> | null> => {
    try {
        const mime = file.type || getMimeType(file.name);
        const url = URL.createObjectURL(file);

        console.log("Loaded file:", file.name, "with MIME type:", mime);

        return { fileName: file.name, url };
    } catch (err) {
        console.error("Error reading file:", err);
    }

    return null;
};

export const onDrop = async (file: File) => {
    // const data = await LoadingActions.wrap(
    //     loadFile(file),
    //     'Processing file...'
    // );
    // if (!data) return;
    selectedFile.file = file;
};

export const onFileSelect = (event: Event) => {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    selectedFile.file = file;

    // const url = URL.createObjectURL(file);
    // setSelectedFile(file.name, url);
};
