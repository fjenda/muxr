<script lang="ts">
    import { onMount } from "svelte";
    import { Button } from "$components";
    import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
    import { faForward, faBackward, faPlay, faPause, faVolumeUp, faVolumeMute } from "@fortawesome/free-solid-svg-icons";

    import 'simplebar';
    import 'simplebar-core/dist/simplebar.css';
    import ResizeObserver from "resize-observer-polyfill";
    import { createDebounce } from "$utils/debounce";
    import type { TrackState } from "$lib/types/TrackState";
    import { trackUrls } from "$stores/trackUrls.svelte.js";
    window.ResizeObserver = ResizeObserver;

    interface AudioPlayerProps {
        fileState: {
            name: string | null;
            url: string | null;
        };
        barHeight?: number;
    }

    let { fileState, barHeight = 128 }: AudioPlayerProps = $props();

    let player: Multitrack | null = null;
    let volumeInput: HTMLInputElement;
    let waveformContainer: HTMLDivElement;
    let waveformScrollContainer: HTMLDivElement;

    let playing = $state(false);
    let time = $state(0);
    let trackStates = $state<TrackState[]>([]);
    let masterVolume = $state(1);

    // const loadUrl = async (url: string) => {
    //     if (!player) return;
    //     await player.addTrack();
    // };

    const backward = () => {
        if (!player) return;
        player.setTime(player.getCurrentTime() - 5);
        getTime();
    }

    const forward = () => {
        if (!player) return;
        player.setTime(player.getCurrentTime() + 5);
        getTime();
    };

    const togglePlay = () => {
        if (!player) return;
        player.isPlaying() ? player.pause() : player.play();
        playing = player.isPlaying();
    };

    const toggleSolo = (index: number) => {
        trackStates[index].solo = !trackStates[index].solo;
        updateTrackVolumes();
    };

    const toggleMute = (index: number) => {
        trackStates[index].mute = !trackStates[index].mute;
        updateTrackVolumes();
    };

    const updateTrackVolumes = () => {
        if (!player) return;

        const anySolo = trackStates.some(ts => ts.solo);
        trackStates.forEach((state, index) => {
            if (state.mute || (anySolo && !state.solo)) {
                player.setTrackVolume(index, 0);
            } else {
                player.setTrackVolume(index, masterVolume);
            }
        });
    };

    const setVolume = () => {
        if (!player) return;
        masterVolume = volumeInput.valueAsNumber;
        updateTrackVolumes();
    }

    // TODO: This currently just replaces the one and only track that's in the list.
    // I will probably keep it like that and allow user to configure what he wants it to split into.
    // TODO: @bug This also resets the volume
    // const loadUrl = async (url: string) => {
    //     if (!player) return;
    //     const track = {
    //         id: trackCount,
    //         draggable: false,
    //         startPosition: 0,
    //         url: url,
    //     };
    //
    //     player.addTrack(track);
    // };

    const formatTime = (seconds: number): string => {
        const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
        const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
        return `${minutes}:${secs}`;
    }

    const onKeyDown = (e: KeyboardEvent) => {
        if (!player) return;

        switch (e.key) {
            case ' ': togglePlay(); break;
            case 'ArrowLeft': backward(); break;
            case 'ArrowRight': forward(); break;
            case 'ArrowUp':
                volumeInput.valueAsNumber = Math.min(1, volumeInput.valueAsNumber + 0.05);
                setVolume();
                break;
            case 'ArrowDown':
                volumeInput.valueAsNumber = Math.max(0, volumeInput.valueAsNumber - 0.05);
                setVolume();
                break;
            default:
                return; // Ignore other keys
        }
    }

    // TODO: replace tracks with stems from backend.
    const initMultitrack = (time: number = 0) => {
        if (player) player.destroy();

        trackStates = [
            ...trackUrls.tracks.map((track, index) => ({
                id: index,
                title: track.title,
                solo: false,
                mute: false,
            }))
        ];

        player = Multitrack.create(
            [
                ...trackUrls.tracks.map((track, index) => ({
                    id: index,
                    draggable: false,
                    startPosition: 0,
                    url: track.url,
                    options: {
                        height: barHeight,
                    },
                }))
            ],
            {
                container: waveformContainer,
                cursorColor: window.matchMedia('(prefers-color-scheme: dark)').matches ? "var(--text-color-dark)" : "var(--text-color-light)"
            }
        );


        console.log(trackUrls.tracks);

        player.once('canplay', () => {
            player.setTime(time);
            playing ? player.play() : player.pause();
            updateTrackVolumes();
        });
    };

    const getTime = () => {
        if (!player) return;
        time = player.getCurrentTime();
    };

    onMount(() => {
        initMultitrack();

        let resizeTimeout = createDebounce(100);
        const resizeObserver = new ResizeObserver(() => {
            resizeTimeout(() => {
                if (!player) return;
                initMultitrack(player.getCurrentTime());
            });
        });

        let timeInterval = setInterval(() => {
            if (player && player.isPlaying()) {
                time = player.getCurrentTime();
            }
        }, 250);

        if (waveformScrollContainer) resizeObserver.observe(waveformScrollContainer);
        if (waveformContainer) waveformContainer.addEventListener('click', getTime);

        return () => {
            clearInterval(timeInterval);
            resizeObserver.disconnect();
            waveformContainer.removeEventListener('click', getTime);
            player?.destroy();
            player = null;
        };
    });
</script>

<svelte:window onkeydown={onKeyDown} />
<div class="audio-player">
    <div class="waveform-scroll-wrapper" bind:this={waveformScrollContainer} data-simplebar>
        <div class="waveform-grid">
            <div class="track-controls-panel">
                {#each trackStates as state, i}
                    <div class="title">
                        <p>{state.title}</p>
                    </div>
                    <div class="track-control" style="height: {barHeight}px;">
                        <Button
                                small
                                class="solo-btn"
                                data-active={state.solo}
                                onClick={() => toggleSolo(i)}
                                aria-label={state.solo ? "Un-solo track" : "Solo track"}
                        >
                            S
                        </Button>
                        <Button
                                small
                                class="mute-btn"
                                data-active={state.mute}
                                onClick={() => toggleMute(i)}
                                aria-label={state.mute ? "Unmute track" : "Mute track"}
                        >
                            {#if state.mute}
                                <FontAwesomeIcon icon={faVolumeMute} />
                            {:else}
                                <FontAwesomeIcon icon={faVolumeUp} />
                            {/if}
                        </Button>
                    </div>
                {/each}
            </div>
            <div class="waveform-container-wrapper">
                <div id="waveform" class="waveform-container" bind:this={waveformContainer}></div>
            </div>
        </div>
    </div>
    <div class="timeline-controls">
        <div class="range-wrapper">
            <label for="volume">Volume</label>
            <input id="volume" type="range" min="0" max="1" value="1" step="0.01" bind:this={volumeInput} oninput={setVolume} />
            <p>{formatTime(time)}</p>
        </div>
        <div class="button-group">
            <Button onClick={backward} tabindex="1">
                <FontAwesomeIcon icon={faBackward} />
            </Button>
            <Button onClick={togglePlay} tabindex="2">
                {#if playing}
                    <FontAwesomeIcon icon={faPause} fixedWidth={true} />
                {:else}
                    <FontAwesomeIcon icon={faPlay} fixedWidth={true} />
                {/if}
            </Button>
            <Button onClick={forward} tabindex="3">
                <FontAwesomeIcon icon={faForward} />
            </Button>
        </div>
    </div>
</div>

<style>
    .audio-player {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        align-items: center;
        width: 100%;
        height: 100%;
        margin: auto;
        background-color: transparent;
        border-radius: 0.5rem;
        padding: 1rem;
    }

    .range-wrapper {
        display: flex;
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;
        gap: 1rem;

        background-color: var(--element-color-light);
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color-light);
    }

    .range-wrapper label {
        white-space: nowrap;
    }

    .button-group {
        display: flex;
        height: 100%;
        align-items: center;
        justify-content: center;
        gap: 1rem;

        background-color: var(--element-color-light);
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color-light);
    }

    .timeline-controls {
        display: flex;
        align-items: center;
        gap: 1rem;
        width: 100%;
        max-width: 800px;
        justify-content: center;
    }

    input[type="range"] {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        background-color: transparent;
    }

    input[type="range"]::-webkit-slider-runnable-track {
        height: 3px;
        background: linear-gradient(
                to right,
                rgb(75, 75, 75) 0%,
                rgb(137, 137, 137) 50%,
                rgb(200, 200, 200) 100%
        );
    }

    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        border: 2px solid var(--border-color-light);
        border-radius: 50%;
        height: 20px;
        width: 20px;
        position: relative;
        bottom: 8px;
        background: var(--element-color-light);
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.4);
        background-size: 50%;
        cursor: grab;
    }

    input[type="range"]:active::-webkit-slider-thumb {
        cursor: grabbing;
    }

    .waveform-scroll-wrapper {
        width: 100%;
        flex-grow: 1;
        height: auto;
        position: relative;
    }

    .waveform-grid {
        display: grid;
        grid-template-columns: auto 1fr;
        width: fit-content;
        min-width: 100%;
    }

    .track-controls-panel {
        display: flex;
        flex-direction: column;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin-right: 0.5rem;
        background-color: var(--element-color-light);
        z-index: 2;
    }

    .track-control {
        display: flex;
        /*flex-direction: column;*/
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.5rem;
        border-bottom: 1px solid var(--border-color-light);
    }

    .track-control:last-child {
        border-bottom: none;
    }

    :global(.solo-btn), :global(.mute-btn) {
        width: 32px;
        height: 32px;
        padding: 0 !important;
        display: block !important;
    }

    :global(.solo-btn[data-active="true"]), :global(.mute-btn[data-active="true"]) {
        background-color: #858585;
        color: white;
    }


    .waveform-container-wrapper {
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    /* The actual waveform container */
    .waveform-container {
        min-width: 100%;
        min-height: 100%;
        display: inline-block;
    }

    #waveform {
        /*width: 100%;*/
        flex-grow: 1;
        position: relative;
    }

    #waveform > :global(div) {
        overflow: hidden !important;
    }

    @media screen and (max-width: 650px) {
        .audio-player {
            padding: 0.5rem;
        }

        .timeline-controls {
            flex-direction: column;
            gap: 0.5rem;
        }

        .button-group {
            width: 100%;
        }
    }

    @media screen and (prefers-color-scheme: dark) {
        .range-wrapper {
            background-color: var(--accent-color-dark);
            border: 1px solid var(--border-color-dark);
        }

        .button-group {
            background-color: var(--accent-color-dark);
            border: 1px solid var(--border-color-dark);
        }

        input[type="range"]::-webkit-slider-thumb {
            border-color: var(--border-color-dark);
            background: var(--element-color-dark);
        }

        input[type="range"]::-webkit-slider-runnable-track {
            background: linear-gradient(
                    to right,
                    rgb(200, 200, 200) 0%,
                    rgb(137, 137, 137) 50%,
                    rgb(75, 75, 75) 100%
            );
        }

        .track-controls-panel {
            background-color: var(--accent-color-dark);
            border-right-color: var(--border-color-dark);
        }

        .track-control {
            border-bottom-color: var(--border-color-dark);
        }

        :global(.solo-btn[data-active="true"]), :global(.mute-btn[data-active="true"]) {
            background-color: var(--accent-color-light);
            color: black;
        }
    }
</style>

