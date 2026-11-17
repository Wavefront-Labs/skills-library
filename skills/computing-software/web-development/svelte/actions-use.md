---
id: computing-software.web-development.svelte.actions-use
name: actions-use
category: computing-software
field: web-development
product: svelte
tags: [use-directive, actions, action-typing, svelte-action, legacy-action-update]
level: practitioner
status: docs-checked
description: "Svelte actions with use:: run once on mount, setup and teardown through $effect, argument handling, typing with Action, and why attachments are preferred from 5.29."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/13-use.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Actions are functions called when an element is mounted, added with `use:`. In Svelte 5.29 and newer consider attachments instead (more flexible and composable). Actions typically use `$effect` to reset state on unmount:

```svelte
<script>
  /** @type {import('svelte/action').Action} */
  function myaction(node) {
    $effect(() => {
      // setup goes here
      return () => {
        // teardown goes here
      };
    });
  }
</script>

<div use:myaction>...</div>
```

With an argument: `function myaction(node, data)` used as `use:myaction={data}`. The action is called only once, not during server-side rendering, and does not run again if the argument changes.

Legacy: before `$effect`, actions returned an object with `update` (called with the latest argument) and `destroy`. Effects are preferred.

Typing: `Action` takes three optional type arguments: a node type (`Element` for everything), a parameter, and custom event handlers the action creates.

```svelte
/** @type {import('svelte/action').Action<HTMLDivElement, undefined, { onswipeleft: (e: CustomEvent) => void }>} */
function gestures(node) {}
```

Then `<div use:gestures onswipeleft={next}>` is typed.

## Checked

2026-11-08. Read the use: page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
