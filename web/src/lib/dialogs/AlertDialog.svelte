<script lang="ts">
	import { Button } from '$components';

	interface AlertDialogProps {
		title: string;
		message: string;
		onConfirm: () => void;
		onCancel: () => void;
	}

	let { title, message, onConfirm, onCancel }: AlertDialogProps = $props();
</script>

<div class="alert-dialog">
	<h2>{title}</h2>
	<p>{message}</p>
	<div class="actions">
		<Button onClick={onConfirm} tabindex="0">Confirm</Button>
		<Button onClick={onCancel} tabindex="1">Cancel</Button>
	</div>
</div>

<style>
	.alert-dialog {
		padding: 2rem;
		min-width: 300px;
		max-width: 90vw;
	}

	h2 {
		margin-block: 0 0.5rem;
	}

	.actions {
		display: flex;
		justify-content: flex-end;
		margin-top: 1.5rem;
		gap: 1rem;
	}
</style>
