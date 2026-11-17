---
id: computing-software.web-development.svelte.bind-dimensions-this
name: bind-dimensions-this
category: computing-software
field: web-development
product: svelte
tags: [bind-this, bind-client-width, resize-observer, component-instance-binding, bindable-props]
level: practitioner
status: docs-checked
description: "Svelte readonly dimension bindings via ResizeObserver, bind:this for DOM nodes and component instances, and bind: on component props marked $bindable."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/12-bind.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dimensions: all visible elements have readonly bindings measured with a `ResizeObserver`: `clientWidth`, `clientHeight`, `offsetWidth`, `offsetHeight`, `contentRect`, `contentBoxSize`, `borderBoxSize`, `devicePixelContentBoxSize`.

```svelte
<div bind:offsetWidth={width} bind:offsetHeight={height}>
  <Chart {width} {height} />
</div>
```

`display: inline` elements have no width or height (except intrinsic ones like `<img>` and `<canvas>`) and cannot be observed; change `display`, for example to `inline-block`. CSS transformations do not trigger `ResizeObserver` callbacks.

`bind:this={dom_node}` gives a reference to a DOM node. It is `undefined` until the component mounts, so read it in an effect or event handler, not during initialisation:

```svelte
<script>
  let canvas;
  $effect(() => { const ctx = canvas.getContext('2d'); });
</script>
<canvas bind:this={canvas}></canvas>
```

It also works on components: `<ShoppingCart bind:this={cart} />` then `cart.empty()` calls an exported function of the child. With function bindings, the getter is required so the right value is nulled on destruction.

Component props: `<Keypad bind:value={pin} />` works for props declared with `$bindable()`. Reactivity otherwise flows only downward. A bindable fallback applies only when unbound; when bound, the parent must not pass `undefined` or a runtime error is thrown.

## Checked

2026-11-08: Read the bind page sections on dimensions, bind:this and component bindings (ResizeObserver bindings, inline-display note, bind:this timing, function-binding getter note, bindable fallback error). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
