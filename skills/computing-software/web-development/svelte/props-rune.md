---
id: computing-software.web-development.svelte.props-rune
name: props-rune
category: computing-software
field: web-development
product: svelte
tags: [props-rune, component-props, destructuring-props, fallback-values, rest-props]
level: intro
status: docs-checked
description: "Receive component inputs with the $props rune: destructuring, fallback values, renaming reserved words, and rest props."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/05-%24props.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pass props like attributes: `<MyComponent adjective="cool" />`. Receive them with `$props`:

```svelte
<script>
  let props = $props();          // props.adjective
  let { adjective } = $props();  // more common
</script>
```

Fallback values apply when the parent does not set a prop or passes `undefined`:

```js
let { adjective = 'happy' } = $props();
```

Fallbacks are not turned into reactive state proxies.

Renaming, needed for invalid identifiers or JavaScript keywords such as `super`:

```js
let { super: trouper = 'lights are gonna find me' } = $props();
```

Rest props collect the remainder:

```js
let { a, b, c, ...others } = $props();
```

Without destructuring you get everything in one object (`let props = $props()`).

Related: `props-updating` for override and mutation rules, `props-types-id` for typing.

## Checked

2026-11-08. Read the $props page in full. Removed an unsupported claim that `let props = $props()` replaces Svelte 4's `$$props` (the page does not say so); the rest matched.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
