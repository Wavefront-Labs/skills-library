---
id: computing-software.web-development.svelte.custom-elements
name: custom-elements
category: computing-software
field: web-development
product: svelte
tags: [custom-elements, web-components, element-constructor, wrapper-lifecycle, connected-callback]
level: advanced
status: docs-checked
description: "Compile Svelte components to custom elements: customElement compiler option and tag, the static element property, props as DOM properties, and the wrapper lifecycle."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/04-custom-elements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Compile with the `customElement: true` compiler option and name the tag via `<svelte:options>`. Use `$host` to access the host element.

```svelte
<svelte:options customElement="my-element" />
<script>
  let { name = 'world' } = $props();
</script>
<h1>Hello {name}!</h1>
<slot />
```

Omit the tag for inner components you do not expose. Consumers can name them later via the static `element` property: `customElements.define('my-element', MyElement.element);`. Then it works as a DOM element, including slotted content.

Props are exposed as DOM properties (and readable/writable as attributes where possible): `el.name = 'everybody'` updates the shadow DOM. List props explicitly; `let props = $props()` without declaring them in the component options means Svelte cannot know which to expose.

Lifecycle (wrapper approach, so the inner component does not know it is a custom element):
- The Svelte component is created in the next tick after `connectedCallback`. Properties set before insertion are saved and applied on creation, but exported functions are only available after mount; use the `extend` option to call them earlier.
- Shadow DOM reflects creates or updates in the next tick, batching updates and avoiding unmounting during synchronous DOM moves.
- The inner component is destroyed in the next tick after `disconnectedCallback`.

See `custom-elements-options` for options and caveats.

## Checked

Method: docs-only read of cited pages, 2026-11-08
