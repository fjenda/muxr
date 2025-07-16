
export enum StemType {
    VOCALS = 'Vocals',
    DRUMS = 'Drums',
    BASS = 'Bass',
    OTHER = 'Other',
    GUITAR = 'Guitar',
    PIANO = 'Piano',
}

export const configurationState = $state({
    twoStems: false as boolean,
    pickedStem: null as StemType | null,
});