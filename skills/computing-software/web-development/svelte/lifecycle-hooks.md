---
id: computing-software.web-development.svelte.lifecycle-hooks
name: lifecycle-hooks
category: computing-software
field: web-development
product: svelte
tags: [onmount, ondestroy, tick, before-update-deprecated, after-update-deprecated]
level: practitioner
status: docs-checked
description: "Svelte 5 lifecycle is only creation and destruction: onMount with sync cleanup return, onDestroy (the only hook on the server), tick, and replacing beforeUpdate/afterUpdate."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/03-lifecycle-hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In Svelte 5 a component's lifecycle has two parts: creation and destruction. State updates in between notify only the render effects that need to react, so there is no "before update" or "after update" hook.

`onMount(fn)`: runs once the component is mounted to the DOM. Call it during initialisation (it may live in an external module). It does not run on the server. A returned function runs on unmount, but only when the callback is synchronous, because `async` functions return a Promise.

```svelte
<script>
  import { onMount } from 'svelte';
  onMount(() => {
    const interval = setInterval(() => console.log('beep'), 1000);
    return () => clearInterval(interval);
  });
</script>
```

`onDestroy(fn)`: runs immediately before unmount. Of `onMount`, `beforeUpdate`, `afterUpdate` and `onDestroy`, it is the only one that runs in a server-side component.

`tick()`: returns a promise resolving once pending state changes are applied, or in the next microtask if none.

Deprecated: `beforeUpdate`/`afterUpdate` are shimmed for compatibility but unavailable in components using runes. Use `$effect.pre` instead of `beforeUpdate` and `$effect` instead of `afterUpdate`; reference the state you care about inside the effect (e.g. `messages;` for an autoscrolling chat) so it does not rerun for unrelated changes like a theme toggle.

## Checked

2026-11-08: Read the Lifecycle hooks page (creation and destruction only, onMount rules and async note, onDestroy on the server, tick, deprecated beforeUpdate and afterUpdate, effect.pre chat example). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
