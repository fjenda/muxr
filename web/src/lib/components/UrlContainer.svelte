<script lang="ts">
  import { goto } from "$app/navigation";
  import { faLink } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
  import { fileState } from '$stores/selectedFile.svelte';

  let youtubeUrl = "";

  const handleSubmit = () => {
    if (!youtubeUrl.trim()) return;
    fileState.url = youtubeUrl.trim();
    fileState.file = null;
    goto("/configure");
  };

</script>

<div class="url-container">
  <FontAwesomeIcon icon={faLink} size="4x" />
  <span>
    <h2>Paste a YouTube URL</h2>
    <p>We'll download and process it for you.</p>
  </span>
  <input
    type="text"
    bind:value={youtubeUrl}
    placeholder="https://www.youtube.com/watch?v=..."
    class="url-input"
    on:keydown={(e) => {
      if (e.key === 'Enter') {
        handleSubmit();
      }
    }}

  />
  <button class="submit-button" on:click={handleSubmit}>
    Use this link
  </button>
</div>

<style lang="scss">
  .url-container {
    border: 2px solid var(--border-color-light);
    background-color: var(--element-color-light);
    border-radius: 0.5rem;
    padding: 4rem 2rem;
    width: 100%;
    max-width: 600px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;

    .url-input {
      width: 100%;
      max-width: 400px;
      padding: 0.5rem 1rem;
      font-size: 1rem;
      border-radius: 20px;
      border: 1px solid #ccc;
    }

    .submit-button {
      background-color: var(--accent-color-light);
      color: var(--text-color-light);
      border: none;
      padding: 0.5rem 1.5rem;
      border-radius: 20px;
      cursor: pointer;
    }

    :global(html.dark-mode) & {
      border-color: var(--border-color-dark);
      background-color: var(--element-color-dark);
    }
  }
</style>
