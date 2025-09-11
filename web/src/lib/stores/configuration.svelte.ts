export enum StemType {
	VOCALS = 'Vocals',
	DRUMS = 'Drums',
	BASS = 'Bass',
	OTHER = 'Other',
	GUITAR = 'Guitar',
	PIANO = 'Piano'
}

export enum FileType {
	MP3 = 'mp3',
	WAV = 'wav',
	FLAC = 'flac'
}

export const configurationState = $state({
	twoStems: false as boolean,
	pickedStem: null as StemType | null,
	outputFileType: FileType.MP3 as FileType
});
