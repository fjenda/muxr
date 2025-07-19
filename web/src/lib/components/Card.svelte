<script lang="ts">
    import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
    import { getWaveformColor } from "$utils/getWaveformColor";

    interface CardProps {
        icon: IconDefinition;
        title: string;
        selected: boolean;
        onClick: () => void;
        children?: any;
    }

    let { icon, title, selected = false, onClick, children }: CardProps = $props();
</script>

<div class="card" class:highlighted={selected} onclick={onClick} role="button" tabindex="0"
     style={getWaveformColor(title) ? `--waveform-color: ${getWaveformColor(title)}` : undefined}
>
    <div class="icon">
        <FontAwesomeIcon icon={icon} size="3x"/>
    </div>
    <h3 class="title">{title}</h3>
    {#if children}
        <div class="card-children">
            {@render children()}
        </div>
    {/if}
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
    background: linear-gradient(135deg, rgba(24, 24, 24, 0.6), rgba(32, 28, 28, 0.4));
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);

    &:hover {
      background: linear-gradient(135deg, rgba(32, 32, 32, 0.6), rgba(40, 36, 36, 0.4));
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border: 1px solid var(--waveform-color, rgba(255, 255, 255, 0.15));
    }

    &:active {
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }

    &.highlighted {
      background: linear-gradient(135deg, rgba(60, 50, 60, 0.4), rgba(45, 40, 40, 0.3));
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border: 1px solid var(--waveform-color, rgba(255, 255, 255, 0.2));
    }


    @media screen and (prefers-color-scheme: light) {
      background: rgba(255, 255, 255, 0.15);
      color: $text-light;
      border: 1px solid rgba(0, 0, 0, 0.08);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

      &:hover {
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12);
        border: 1px solid rgba(0, 0, 0, 0.15);
      }

      &.highlighted {
        background: rgba(255, 255, 255, 0.25);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
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
