---
id: computing-software.web-development.svelte.scoped-styles
name: scoped-styles
category: computing-software
field: web-development
product: svelte
tags: [scoped-styles, component-css, specificity, scoped-keyframes, style-element]
level: intro
status: docs-checked
description: "How Svelte scopes component CSS with a hashed class, the 0-1-0 specificity bump and :where for repeats, scoped @keyframes, and nested style elements."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/04-styling/01-scoped-styles.md
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/04-styling/04-nested-style-elements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A component's `<style>` is scoped by default: it does not apply to elements outside the component. Svelte adds a class based on a hash of the component styles (e.g. `svelte-123xyz`) to affected elements.

```svelte
<style>
  p {
    /* this will only affect <p> elements in this component */
    color: burlywood;
  }
</style>
```

Specificity: each scoped selector gains 0-1-0 from the scoping class, so a component's `p` selector beats a global stylesheet's `p` even if the global sheet loads later. When the class must be added several times to one selector, later occurrences use `:where(.svelte-xyz123)` so specificity does not increase further.

Keyframes: `@keyframes` names are scoped with the same hashing, and `animation` rules in the component are adjusted to match.

```svelte
<style>
  .bouncy { animation: bounce 10s; }
  /* only accessible inside this component */
  @keyframes bounce { /* ... */ }
</style>
```

Only one top-level `<style>` per component is allowed. A `<style>` nested inside elements or logic blocks is inserted as-is into the DOM with no scoping or processing, so `div { color: red; }` there applies to all divs in the DOM.

See `global-styles` to escape scoping.

## Checked

2026-11-08: Read the scoped styles and nested style elements pages (hash class, 0-1-0 specificity, :where for repeats, scoped keyframes, one top-level style, nested style inserted as-is). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
