<script lang="ts">
    let { onClick, children, ...rest } = $props();
</script>

<button onclick={onClick} {...rest}>
    {@render children()}
</button>

<style>
    button {
        border-radius: 0.35rem;
        border: 1px solid transparent;
        padding: 0.6em 1.2em;
        font-size: 1em;
        color: var(--text-color-light);
        background-color: #eaeaea;
        transition: border-color 0.15s ease-in-out,
                    background-color 0.15s ease-in-out,
                    box-shadow 0.15s ease-in-out;
        box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
        cursor: pointer;
        outline: none;
        display: flex;
    }

    button:active,
    button:focus-within,
    button:focus,
    button:hover {
        border-color: var(--border-color-light);
    }

    button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    button:disabled:hover {
        border-color: transparent;
    }

    @media (prefers-color-scheme: dark) {
        button {
            color: var(--text-color-dark);
            background-color: #303030;
        }

        button:active,
        button:focus-within,
        button:focus,
        button:hover {
            border-color: var(--border-color-dark);
        }
    }
</style>