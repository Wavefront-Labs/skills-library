---
id: computing-software.web-development.svelte.svelte-options
name: svelte-options
category: computing-software
field: web-development
product: svelte
tags: [svelte-options, runes-mode-flag, css-injected, namespace-option, customelement-option]
level: practitioner
status: docs-checked
description: "Per-component compiler options with svelte:options: runes true/false, namespace, customElement, css injected, and the deprecated immutable and accessors."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/05-special-elements/07-svelte-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`<svelte:options option={value} />` sets per-component compiler options (detailed under the compiler `compile` docs):

- `runes={true}` forces runes mode; `runes={false}` forces legacy mode.
- `namespace="..."`: where the component is used; `"html"` (default), `"svg"` or `"mathml"`.
- `customElement={...}`: options used when compiling as a custom element. A string is used as the `tag` option.
- `css="injected"`: the component injects its styles inline. During server-side rendering it is a `<style>` tag in the `head`; on the client it is loaded via JavaScript.

```svelte
<svelte:options customElement="my-custom-element" />
```

Deprecated from Svelte 4, non-functional in runes mode:
- `immutable={true}`: never mutate, so the compiler can use simple referential equality checks. `immutable={false}` (default) is more conservative.
- `accessors={true}` adds getters and setters for the component's props; `accessors={false}` is the default.

See `custom-elements` for the full custom element options.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the svelte:options page: runes, namespace, customElement, css="injected" and the deprecated immutable and accessors options. Nothing removed.
