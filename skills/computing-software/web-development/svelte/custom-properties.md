---
id: computing-software.web-development.svelte.custom-properties
name: custom-properties
category: computing-software
field: web-development
product: svelte
tags: [css-custom-properties, component-theming, svelte-css-wrapper, var-fallback, display-contents]
level: practitioner
status: docs-checked
description: "Pass static or dynamic CSS custom properties to Svelte components as --prop attributes, the wrapper element they generate, reading with var(), and a layout caveat."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/04-styling/03-custom-properties.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pass CSS custom properties, static or dynamic, to a component:

```svelte
<Slider
  bind:value
  min={0}
  max={100}
  --track-color="black"
  --thumb-color="rgb({r} {g} {b})"
/>
```

This desugars to a wrapper element:

```svelte
<svelte-css-wrapper style="display: contents; --track-color: black; --thumb-color: rgb({r} {g} {b})">
  <Slider bind:value min={0} max={100} />
</svelte-css-wrapper>
```

For an SVG element it uses `<g>` instead (with the style but no `display: contents`).

Inside the component, read them with `var(...)` and give fallbacks:

```svelte
<style>
  .track { background: var(--track-color, #aaa); }
  .thumb { background: var(--thumb-color, blue); }
</style>
```

You do not have to set values directly on the component; any parent element defining the properties works. It is common to define them on `:root` in a global stylesheet.

Caveat: the extra element does not affect layout, but it does affect CSS selectors that use the `>` combinator to target an element directly inside the component's container.

## Checked

Read the full styling custom-properties page. Confirmed the --prop attribute syntax, the svelte-css-wrapper with display: contents, the SVG g variant, var() fallbacks, definition on a parent or :root, and the combinator caveat. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
