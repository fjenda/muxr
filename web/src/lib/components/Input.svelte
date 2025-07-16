<script lang="ts">
    interface InputProps {
        id: string;
        placeholder?: string;
        value?: string;
    }

    let { id, placeholder, value }: InputProps = $props();
</script>

<input id={id} placeholder={placeholder} bind:value={value} />

<style>
    input {
        border-radius: 8px;
        border: 1px solid transparent;
        padding: 0.6em 1.2em;
        font-size: 1em;
        font-weight: 500;
        font-family: inherit;
        color: #0f0f0f;
        background-color: #ffffff;
        transition: border-color 0.25s;
        box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
        outline: none;
    }

    @media (prefers-color-scheme: dark) {
        input {
            color: #ffffff;
            background-color: #0f0f0f98;
        }
    }
</style>