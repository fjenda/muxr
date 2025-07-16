<script lang="ts">
    import { LoadingIndicator } from "$components";
    import { loading, LoadingActions } from './loading.svelte.js';

    export { loading, LoadingActions } from './loading.svelte.js';
</script>

<slot />
<LoadingIndicator />