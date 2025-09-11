<script lang="ts">
    import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import { getWaveformColor } from "$utils/getWaveformColor";


    export let icon: IconDefinition;
    export let title: string;
    export let selected: boolean = false;
    export let onClick: () => void;
</script>

<div class="card" class:highlighted={selected} onclick={onClick} onkeydown="{onClick}" role="button" tabindex="0"
     style={getWaveformColor(title) ? `--waveform-color: ${getWaveformColor(title)}` : undefined}
>
    <div class="icon">
        <FontAwesomeIcon icon={icon} size="3x"/>
    </div>
    <h3 class="title">{title}</h3>
    <slot />
</div>

<style lang="scss">
  $blur: 8px;
  $radius: 0.5rem;
  $padding: 2rem;
  $gap: 1rem;
  $text-dark: var(--text-color-dark);
  $text-light: var(--text-color-light, #222);

  .card {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    padding: $padding;
    gap: $gap;
    border-radius: $radius;
    transition: background 0.3s ease,
    box-shadow 0.3s ease,
    transform 0.2s ease,
    border 0.3s ease;
    color: $text-dark;
    backdrop-filter: blur($blur);
    -webkit-backdrop-filter: blur($blur);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);

    &::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(32, 32, 32, 0.6), rgba(40, 36, 36, 0.4));
      opacity: 0.5;
      transition: opacity 0.3s ease;
      z-index: 0;
      border-radius: $radius;
    }

    > * {
      position: relative;
      z-index: 1;
    }

    &:hover {
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border: 1px solid var(--waveform-color, rgba(255, 255, 255, 0.15));

      &::before {
        opacity: 1;
      }
    }

    &.highlighted {
      background: linear-gradient(135deg, rgb(69 69 69 / 40%), rgba(45, 40, 40, 0.3));
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border: 1px solid var(--waveform-color, rgba(255, 255, 255, 0.2));
      &::before {
        opacity: 0.5;
      }
    }

      :global(html:not(.dark-mode)) & {
          background: rgba(255, 255, 255, 0.9);
          color: $text-light;
          border: 1px solid rgba(0, 0, 0, 0.08);
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);

          &::before {
              background: linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(240, 240, 240, 0.2));
              opacity: 0.6;
          }

          &:hover {
              background: rgba(255, 255, 255, 1);
              box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
              border: 1px solid var(--waveform-color, rgba(0, 0, 0, 0.1));
          }

          &.highlighted {
              background: linear-gradient(135deg, rgba(240, 240, 240, 0.8), rgba(220, 220, 220, 0.7));
              border: 1px solid var(--waveform-color, rgba(0, 0, 0, 0.12));
              box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
          }
      }


      @media screen and (max-width: 650px) {
      padding: 1rem;
      gap: 0.5rem;
    }
  }

  .title {
    pointer-events: none;
    text-align: center;
  }

</style>
