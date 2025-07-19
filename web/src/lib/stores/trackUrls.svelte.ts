export interface Track {
    title: string,
    url: string,
}

export const trackUrls = $state({
    // a.click() will go here
    downloadZip: () => {},
    tracks: [] as Track[],
    addUrl: (track: Track) => {
        if (!trackUrls.tracks.includes(track)) {
            trackUrls.tracks.push(track);
        }
    },
    removeUrl: (track: Track) => {
        const index = trackUrls.tracks.indexOf(track);
        if (index !== -1) {
            trackUrls.tracks.splice(index, 1);
        }
    },
    clear: () => {
        trackUrls.tracks = [];
    },
});