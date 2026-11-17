---
id: computing-software.web-development.svelte.custom-elements-options
name: custom-elements-options
category: computing-software
field: web-development
product: svelte
tags: [custom-element-options, shadow-root-option, props-reflect-attribute, extend-option, custom-element-caveats]
level: sme
status: docs-checked
description: "Svelte customElement options object: tag, shadow, props attribute/reflect/type, extend for ElementInternals, plus encapsulation, SSR, slot and event caveats."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/04-custom-elements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pass an object as `customElement` in `<svelte:options>`:

- `tag`: element name; defined in the `customElements` registry on import.
- `shadow`: `"none"` (no shadow root, no encapsulation, no slots), `"open"`, or a `ShadowRootInit` object passed to `attachShadow()`.
- `props`: per prop `attribute` (attribute name; default is the lowercase property name), `reflect` (default false: set true to reflect to the DOM), `type` (`'String'` default, `'Boolean'`, `'Number'`, `'Array'`, `'Object'`). Unlisted props use defaults.
- `extend`: function receiving the generated class and returning a class, e.g. for `ElementInternals` form integration.

```svelte
<svelte:options
  customElement={{
    tag: 'custom-element',
    shadow: { mode: import.meta.env.DEV ? 'open' : 'closed', clonable: true },
    props: { name: { reflect: true, type: 'Number', attribute: 'element-index' } },
    extend: (customElementConstructor) => class extends customElementConstructor {
      static formAssociated = true;
      constructor() { super(); this.attachedInternals = this.attachInternals(); }
    }
  }}
/>
```

TypeScript in `extend` needs `lang="ts"` on one script and erasable syntax only; it is not processed by preprocessors.

Caveats:
- Styles are encapsulated, so global CSS (even `:global(...)`) does not apply unless `shadow: "none"`; styles are inlined as a JS string.
- Not suited to SSR (shadow DOM invisible until JavaScript loads).
- Slotted content renders eagerly in the DOM, even inside `{#if}`.
- `let:` has no effect.
- Context cannot cross custom elements.
- Do not name props starting with `on`; they become event listeners.
- Older browsers need polyfills.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte Custom elements page (Component options and Caveats sections): tag, shadow values, props attribute/reflect/type and defaults, extend, the erasable-syntax note, and every caveat. Nothing removed.
