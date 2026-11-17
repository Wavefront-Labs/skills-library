---
id: computing-software.web-development.svelte.effect-variants
name: effect-variants
category: computing-software
field: web-development
product: svelte
tags: [effect-pre, effect-tracking, effect-pending, effect-root, create-subscriber]
level: advanced
status: docs-checked
description: "The Svelte $effect variants: $effect.pre before DOM updates, $effect.tracking, $effect.pending for in-flight await promises, and $effect.root for manual scopes."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/04-%24effect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`$effect.pre`: works exactly like `$effect` but runs before DOM updates scheduled after it (parent DOM may already be updated). Typical use is measuring the DOM before updating, e.g. autoscroll in a chat window; reference `messages.length` so it re-runs, then `tick().then(...)` to scroll. With await expressions, block updates like `{#if}` and `{#each}` in the same component also run before `$effect.pre`.

`$effect.tracking()`: returns whether code is in a tracking context (effect or template): `false` in component setup, `true` in an effect or `{$effect.tracking()}` in markup. It underpins abstractions like `createSubscriber` (from `svelte/reactivity`), which create listeners only when values are being tracked.

`$effect.pending()`: with `await` in components, returns how many promises are pending in the current boundary, excluding child boundaries.

```svelte
{#if $effect.pending()}
  <p>pending promises: {$effect.pending()}</p>
{/if}
```

`$effect.root(fn)`: creates a non-tracked scope that is not auto-cleaned, for nested effects you control manually, and lets you create effects outside component initialisation. It returns a destroy function:

```js
const destroy = $effect.root(() => { $effect(() => {}); return () => {}; });
destroy();
```

## Checked

2026-11-08. Read the $effect page in full. Claims matched; "measuring the DOM before updating" was an inference from the autoscroll example and is kept only as that example. The createSubscriber module path (svelte/reactivity) comes from the page's link target, not a page of its own.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
