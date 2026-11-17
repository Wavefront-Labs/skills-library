---
id: computing-software.web-development.svelte.effect-avoid
name: effect-avoid
category: computing-software
field: web-development
product: svelte
tags: [effect-antipattern, derived-instead-of-effect, function-bindings, sync-state, effect-loop]
level: practitioner
status: docs-checked
description: "When not to use $effect in Svelte: replace state-syncing effects with $derived, oninput callbacks or function bindings, and break loops with untrack."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/04-%24effect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`$effect` is an escape hatch for things like analytics and direct DOM manipulation. Avoid it to synchronise state.

Instead of this:

```js
let doubled = $state();
$effect(() => { doubled = count * 2; });
```

write `let doubled = $derived(count * 2);` (use `$derived.by` for complex logic). If you wanted to reassign the derived for an optimistic UI, deriveds can be overridden as of Svelte 5.25.

Linked inputs (money spent / money left): rather than two effects updating each other, derive one value and use a function binding on the other input:

```svelte
let spent = $state(0);
let left = $derived(total - spent);
function updateLeft(left) { spent = total - left; }
...
<input type="range" bind:value={() => left, updateLeft} max={total} />
```

`oninput` callbacks also work; function bindings are preferred where possible.

If you must update `$state` inside an effect and hit an infinite loop because you read and write the same state, wrap the read in `untrack`.

## Checked

2026-11-08. Read the $effect page in full. Removed an unsupported summary line; the rest matched the "When not to use $effect" section.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
