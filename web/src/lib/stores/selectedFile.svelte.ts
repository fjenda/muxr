import { writable } from "svelte/store";

export const selectedFile = writable<File | null>(null);
