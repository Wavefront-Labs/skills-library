---
id: computing-software.web-development.svelte.transition-custom
name: transition-custom
category: computing-software
field: web-development
product: svelte
tags: [custom-transition, transition-css-function, transition-tick, easing, crossfade-coordination]
level: advanced
status: docs-checked
description: "Write custom Svelte transition functions: signature, delay, duration, easing, css(t, u) for Web Animations, tick for JS-driven effects, and returning a function."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/14-transition.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Signature:

```js
transition = (node: HTMLElement, params: any, options: { direction: 'in' | 'out' | 'both' }) => {
  delay?: number,
  duration?: number,
  easing?: (t: number) => number,
  css?: (t: number, u: number) => string,
  tick?: (t: number, u: number) => void
}
```

If the returned object has a `css` function, Svelte generates keyframes for a web animation. `t` is between 0 and 1 after `easing`; in transitions run 0 to 1, out transitions 1 to 0, so 1 is the natural state. `u` equals `1 - t`. The function is called repeatedly before the transition begins.

```js
function whoosh(node, params) {
  const existingTransform = getComputedStyle(node).transform.replace('none', '');
  return {
    delay: params.delay || 0,
    duration: params.duration || 400,
    easing: params.easing || elasticOut,
    css: (t, u) => `transform: ${existingTransform} scale(${t})`
  };
}
```

Use it with `<div in:whoosh>`. A `tick` function is called during the transition with the same `t` and `u` (the doc's typewriter example sets `node.textContent`). Prefer `css` over `tick` where possible: web animations can run off the main thread, preventing jank.

If a transition returns a function instead of an object, it is called in the next microtask, which lets several transitions coordinate (crossfade). The third argument `options.direction` is `in`, `out` or `both`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the transition: page: custom transition signature, css(t, u) semantics, tick, preference for css, returning a function (next microtask) and options.direction. Nothing removed.
