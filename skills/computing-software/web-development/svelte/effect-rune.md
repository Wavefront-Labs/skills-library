---
id: computing-software.web-development.svelte.effect-rune
name: effect-rune
category: computing-software
field: web-development
product: svelte
tags: [effect-rune, effect-teardown, effect-dependencies, side-effects, untrack]
level: practitioner
status: docs-checked
description: "How $effect runs in Svelte 5: browser-only timing after mount, batching, teardown functions, synchronous dependency tracking, and conditional dependencies."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/04-%24effect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Effects run when state updates (third-party libraries, `<canvas>`, network requests). They run only in the browser, not during server-side rendering.

Lifecycle: they run after the component mounts, in a microtask after state changes. Re-runs are batched and happen after DOM updates. `$effect` can be called anywhere while a parent effect is running.

Teardown: return a function; it runs immediately before the effect re-runs and when the effect is destroyed.

```js
$effect(() => {
  const id = setInterval(() => count += 1, milliseconds);
  return () => clearInterval(id);
});
```

Dependencies: reactive values (`$state`, `$derived`, `$props`) read synchronously, including via called functions. Values read after an `await` or inside `setTimeout` are not tracked. If `$state`/`$derived` are used directly inside the effect (for example during creation of a reactive class), they are not dependencies.

An effect reruns when the object it read changes (a new object), not when a property inside it is mutated; `$inspect` can observe changes inside an object at dev time. It depends only on what it read on its last run, so in `if (condition) { use(color) } else {...}` the effect ignores `color` while `condition` is false.

Exempt reads with `untrack`. Compare `$:` in Svelte 4: triggering differs.

## Checked

2026-11-08. Read the $effect page in full. Sharpened the "object changes" sentence (the page's example shows a derived that is a new object each time does rerun the effect); other claims matched.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
