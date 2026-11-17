---
id: computing-software.web-development.svelte.animate-directive
name: animate-directive
category: computing-software
field: web-development
product: svelte
tags: [animate-directive, svelte-animate, flip, keyed-each-reorder, custom-animation]
level: practitioner
status: docs-checked
description: "Svelte animate: runs when keyed each items are reordered, must be on an immediate child, takes parameters, and supports custom functions receiving from and to DOMRects."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/16-animate.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An animation triggers when the contents of a keyed each block are re-ordered. It does not run when an item is added or removed, only when the index of an existing item changes. `animate:` must be on an immediate child of a keyed each block.

```svelte
{#each list as item, index (item)}
  <li animate:flip>{item}</li>
{/each}
```

Parameters: `animate:flip={{ delay: 500 }}`. Built-ins come from `svelte/animate`.

Custom animation functions:

```js
animation = (node: HTMLElement, { from: DOMRect, to: DOMRect }, params: any) => {
  delay?: number,
  duration?: number,
  easing?: (t: number) => number,
  css?: (t: number, u: number) => string,
  tick?: (t: number, u: number) => void
}
```

`from` is the element's DOMRect at its start position and `to` its rect after the list has been reordered and the DOM updated. If the result has `css`, Svelte creates a web animation; `t` goes from 0 to 1 after easing and `u` equals `1 - t`. It is called repeatedly before the animation begins.

```js
function whizz(node, { from, to }, params) {
  const dx = from.left - to.left;
  const dy = from.top - to.top;
  const d = Math.sqrt(dx * dx + dy * dy);
  return {
    delay: 0,
    duration: Math.sqrt(d) * 120,
    easing: cubicOut,
    css: (t, u) => `transform: translate(${u * dx}px, ${u * dy}px) rotate(${t * 360}deg);`
  };
}
```

A `tick` function is also allowed; prefer `css`, which can run off the main thread.

## Checked

2026-11-08. Read the animate: page in full. All claims matched; the page links its built-in functions to the svelte/animate docs, which were not separately read.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
