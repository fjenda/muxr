import { processingState } from "./processingState.svelte";

export interface Track {
  title: string;
  url: string;
}

export const trackUrls = $state({
  downloadTrack: (index: number) => {
    const track = trackUrls.tracks[index];
    if (track) {
      const a = document.createElement("a");
      a.href = track.url;
      a.download = `${processingState.sessionId}_${track.title}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } else {
      console.error("Track not found at index:", index);
    }
  },
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
