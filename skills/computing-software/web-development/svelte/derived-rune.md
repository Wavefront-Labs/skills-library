---
id: computing-software.web-development.svelte.derived-rune
name: derived-rune
category: computing-software
field: web-development
product: svelte
tags: [derived-rune, derived-by, computed-state, reactive-dependencies, side-effect-free]
level: intro
status: docs-checked
description: "Compute values from state with $derived and $derived.by in Svelte 5: side-effect-free expressions, tracked dependencies, await tracking, and untrack."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/03-%24derived.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
</script>
```

The expression must be free of side effects; Svelte disallows state changes (like `count++`) inside it. Component code runs once at creation, so without `$derived`, `doubled` would keep its first value. Class fields can be `$derived` too.

`$derived.by(fn)` takes a function for derivations that do not fit in an expression. `$derived(expression)` is equivalent to `$derived.by(() => expression)`.

```js
let total = $derived.by(() => {
  let t = 0;
  for (const n of numbers) t += n;
  return t;
});
```

Dependencies: anything read synchronously in the expression or function body. When one changes, the derived is marked dirty and recalculated on next read. If the expression contains `await`, state read after the `await` is tracked as well (`$derived(await a + b)` tracks `a` and `b`); this does not apply to `await` inside functions the expression calls.

To exempt state from tracking, use `untrack` from `svelte`.

## Checked

2026-11-08. Read the $derived page in full. Every claim matched the page; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
