<script lang="ts">
    import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
    import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";

    interface CardProps {
        icon: IconDefinition;
        title: string;
        selected: boolean;
        onClick: () => void;
        children?: any;
    }

    let { icon, title, selected = false, onClick, children }: CardProps = $props();
</script>

<div class="card" class:highlighted={selected} onclick={onClick} role="button" tabindex="0">
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

<style>
    .card {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
        gap: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease, box-shadow 0.3s ease;

        background-color: rgba(0, 0, 0, 0.2);
        color: var(--text-color-dark);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }

    .card:hover {
        background-color: rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
    }

    .card.highlighted {
        background-color: rgba(0, 0, 0, 0.3);
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
    }

    .title {
        pointer-events: none;
        text-align: center;
    }

    @media screen and (prefers-color-scheme: dark) {
        .card {
            background-color: rgba(255, 255, 255, 0.1);
            color: var(--text-color-dark);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .card:hover {
            background-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .card.highlighted {
            background-color: rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
    }

    @media screen and (max-width: 650px) {
        .card {
            padding: 1rem;
            gap: 0.5rem;
        }
    }
</style>
