<script lang="ts">
  import { DropContainer } from "$components";
</script>

<div class="main-container">
    <h1 class="title">muxr</h1>
    <DropContainer />
</div>

<style>
    .main-container {
        padding: 4rem 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        /*align-items: center;*/
        height: 100vh;
        background-color: var(--bg-color-dark);
    }

    .title {
        text-align: center;
    }
</style>

