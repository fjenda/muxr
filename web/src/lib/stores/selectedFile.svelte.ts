
export const fileState = $state({
    url: null as string | null,
    name: null as string | null,
});

export const setSelectedFile = (name: string, url: string) => {
    if (fileState.url) URL.revokeObjectURL(fileState.url);

    fileState.name = name;
    fileState.url = url;
}

if (typeof window !== 'undefined') {
    window.addEventListener('beforeunload', () => {
        if (fileState.url) URL.revokeObjectURL(fileState.url);
    });
}

export const selectedFile = $state({ file: null as File | null });