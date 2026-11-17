---
id: computing-software.web-development.svelte.derived-semantics
name: derived-semantics
category: computing-software
field: web-development
product: svelte
tags: [derived-override, optimistic-ui, push-pull-reactivity, derived-destructuring, derived-equality]
level: practitioner
status: docs-checked
description: "Svelte $derived behaviours: overriding derived values for optimistic UI (5.25+), objects are not made deeply reactive, destructuring, and push-pull update skipping."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/03-%24derived.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Overriding: you can temporarily reassign a derived (unless declared with `const`). Useful for optimistic UI:

```svelte
let { post, like } = $props();
let likes = $derived(post.likes);

async function onclick() {
  likes += 1;
  try { await like(); } catch { likes -= 1; }
}
```

Prior to Svelte 5.25, deriveds were read-only.

No deep reactivity: unlike `$state`, derived objects and arrays are left as-is. With `let selected = $derived(items[index])`, mutating `selected` affects the underlying `items` array only because `items` itself is deeply reactive state.

Destructuring: `let { a, b, c } = $derived(stuff());` makes each variable a separate derived of the result.

Push-pull: when state changes, dependents are notified immediately (push), but deriveds re-evaluate only when read (pull). If the new value is referentially identical to the old one, downstream updates are skipped, so with `let large = $derived(count > 10)` the button text updates only when `large` flips, not on every `count` change.

## Checked

2026-11-08. Read the $derived page in full. Overriding, 5.25 note, no-deep-reactivity, destructuring and push-pull claims matched the page; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
