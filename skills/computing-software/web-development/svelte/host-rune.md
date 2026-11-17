---
id: computing-software.web-development.svelte.host-rune
name: host-rune
category: computing-software
field: web-development
product: svelte
tags: [host-rune, custom-element-host, dispatch-custom-event, svelte-options-customelement, shadow-host]
level: advanced
status: docs-checked
description: "Use the $host rune in a Svelte component compiled as a custom element to reach the host element and dispatch custom events to the page."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/08-%24host.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a component is compiled as a custom element, `$host()` gives access to the host element, for example to dispatch custom events.

```svelte
<!-- Stepper.svelte -->
<svelte:options customElement="my-stepper" />

<script>
  function dispatch(type) {
    $host().dispatchEvent(new CustomEvent(type));
  }
</script>

<button onclick={() => dispatch('decrement')}>decrement</button>
<button onclick={() => dispatch('increment')}>increment</button>
```

The consumer imports the file (which registers the element) and listens with event attributes:

```svelte
<script>
  import './Stepper.svelte';
  let count = $state(0);
</script>

<my-stepper
  ondecrement={() => count -= 1}
  onincrement={() => count += 1}
></my-stepper>

<p>count: {count}</p>
```

Related: `svelte-options` for the `customElement` option, `custom-elements` for the full feature set.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte `$host` docs page: `$host()` gives the host element when compiling as a custom element, the Stepper/App example, and `<svelte:options customElement="my-stepper" />`. Nothing removed.
