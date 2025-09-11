<script lang="ts">
	import { goto } from '$app/navigation';
	import { faDrum, faMicrophone } from '@fortawesome/free-solid-svg-icons';
	import { Button, Card } from '$components';
	import { configurationState, FileType } from '$stores/configuration.svelte';
	import { separate } from '$utils/separate';
	import { fileState } from '$stores/selectedFile.svelte';

	const options = [
		{ icon: faMicrophone, title: 'Isolate one stem' },
		{ icon: faDrum, title: 'Split the song into all audible stems' }
	];

	let selected = '';
	const handleCardClick = (title: string) => (selected = title);
	const selectFileType = (type: FileType) => (configurationState.outputFileType = type);
	const continueToNext = async () => {
		if (selected === 'Isolate one stem') {
			configurationState.twoStems = true;
			return goto('/configure/isolate');
		}

		await separate(fileState.url);
	};
</script>

<div class="container">
	<div class="header">
		<h2 class="title">Separation type</h2>
	</div>
	<div class="card-grid">
		{#each options as { icon, title } (title)}
			<Card {icon} {title} selected={selected === title} onClick={() => handleCardClick(title)} />
		{/each}
	</div>
	<div id="format-options" role="radiogroup" aria-label="Output format">
		{#each Object.values(FileType) as format (format)}
			<button
				type="button"
				data-format={format}
				class="format-btn"
				class:selected={configurationState.outputFileType === format}
				onclick={() => selectFileType(format)}
			>
				{format}
			</button>
		{/each}
	</div>
	<input type="hidden" name="format" id="format" value="mp3" />

	<div class="button-container">
		<Button onClick={continueToNext} tabindex="0" disabled={!selected}>Continue</Button>
	</div>
</div>

<style lang="scss">
  @use '../../lib/styles/configure' as *;

  #format-options {
    display: flex;
    gap: $gap-sm;
  }

  .format-btn {
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: 500;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: var(--text-color-dark);
    background: linear-gradient(135deg, rgba(24, 24, 24, 0.6), rgba(32, 28, 28, 0.4));
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);

    &:hover,
    &:focus-visible {
      background: linear-gradient(135deg, rgba(32, 32, 32, 0.6), rgba(40, 36, 36, 0.4));
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
      border-color: rgba(255, 255, 255, 0.15);
    }

    &.selected {
      background: linear-gradient(135deg, rgb(69 69 69 / 40%), rgba(45, 40, 40, 0.3));
      box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
      border-color: rgba(255, 255, 255, 0.25);
      color: $text-dark;
    }

    :global(html):not(.dark-mode) & {
      color: $text-light;
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(0, 0, 0, 0.1);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

      &:hover,
      &:focus-visible {
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        border-color: rgba(0, 0, 0, 0.2);
      }

      &.selected {
        background: rgba(255, 255, 255, 0.25);
        border-color: rgba(0, 0, 0, 0.25);
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
        color: $text-light;
      }
    }

    &:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
  }
</style>
