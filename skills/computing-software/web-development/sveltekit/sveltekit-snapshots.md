---
id: computing-software.web-development.sveltekit.sveltekit-snapshots
name: sveltekit-snapshots
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, snapshots, snapshot, navigation, session-storage, form-state, history]
level: intro
status: docs-checked
description: "Preserve ephemeral DOM state such as unsent form input across SvelteKit navigation and reloads with the snapshot helper."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/65-snapshots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep things like half-typed form input or sidebar scroll when the user navigates away and back, or refreshes.

## Use
Call `snapshot` from `$app/navigation` during component initialization:
```svelte
<script>
	import { snapshot } from '$app/navigation';

	let comment = $state('');

	snapshot({
		capture: () => comment,
		restore: (value) => (comment = value)
	});
</script>

<form method="POST">
	<label for="comment">Comment</label>
	<textarea id="comment" bind:value={comment} />
	<button>Post comment</button>
</form>
```
On navigating away (including shallow routing) `capture` runs right before the page updates and its value is tied to the current history entry. On navigating back, `restore` runs with the stored value as soon as the page updates.

## IDs
A snapshot needs a unique ID to survive remounts and reloads. By default it is generated from the stack trace at the `snapshot(...)` call. Pass an explicit `id` to keep it stable across deployments (source changes alter the stack trace), or to tell apart snapshots made through a shared wrapper or by multiple instances of one component:
```js
snapshot({
	id: 'comment',
	capture: () => comment,
	restore: (value) => (comment = value)
});
```

## Reset and storage
- The optional `reset` callback runs on navigations with no captured value to restore, such as when a new history entry is created.
- Values are serialized with devalue (JSON, `Date`, `Map`, plus custom types from the `transport` hook) and persisted to `sessionStorage`, so they survive reloads and returning from another site.
- Avoid returning very large objects from `capture`: captured objects stay in memory for the session and may be too big for `sessionStorage`.

## Legacy form
Previously you exported `const snapshot = { capture, restore }` (typed `import('./$types').Snapshot<string>`) from `+page.svelte` or `+layout.svelte`. It is deprecated; values captured that way are serialized as JSON and shallow navigations do not capture them.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/65-snapshots.md in full, including the legacy snapshot export note. No claims trimmed.
