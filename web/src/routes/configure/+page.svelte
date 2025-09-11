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
</style>
