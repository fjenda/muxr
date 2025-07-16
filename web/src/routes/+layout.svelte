<script>
    import { LoadingProvider, DialogProvider } from "$providers";
    let { children } = $props();
</script>

<LoadingProvider>
    <DialogProvider>
        <main class="container">
            {@render children()}
        </main>
    </DialogProvider>
</LoadingProvider>


<style>
    .container {
        height: 100%;
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }
</style>