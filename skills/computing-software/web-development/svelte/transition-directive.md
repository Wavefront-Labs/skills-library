---
id: computing-software.web-development.svelte.transition-directive
name: transition-directive
category: computing-software
field: web-development
product: svelte
tags: [transition-directive, svelte-transition, local-vs-global-transition, prefers-reduced-motion, transition-events]
level: practitioner
status: docs-checked
description: "Svelte transition: directive: bidirectional enter and leave effects, local default vs |global, parameters, reduced-motion accessibility, and introstart/outroend events."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/14-transition.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A transition triggers when an element enters or leaves the DOM because of a state change. While a block is transitioning out, all elements inside it are kept until every transition in the block finishes. `transition:` is bidirectional: it can reverse smoothly mid-way.

```svelte
<script>
  import { fade } from 'svelte/transition';
  let visible = $state(false);
</script>

{#if visible}
  <div transition:fade>fades in and out</div>
{/if}
```

Local vs global: transitions are local by default and play only when their own block is created or destroyed, not parent blocks. Add `|global` to play when any ancestor block changes:

```svelte
{#if x}
  {#if y}
    <p transition:fade>only when y changes</p>
    <p transition:fade|global>when x or y change</p>
  {/if}
{/if}
```

Parameters are an object literal in the expression tag (the double curlies are not special syntax): `transition:fade={{ duration: 2000 }}`. Built-ins come from `svelte/transition`.

Accessibility: transitions use the Web Animations API, so a global `@media (prefers-reduced-motion: reduce)` rule zeroing `transition-duration` and `animation-duration` has no effect. Use `prefersReducedMotion` from `svelte/motion` to adjust or disable them.

Events (in addition to DOM events): `introstart`, `introend`, `outrostart`, `outroend`, e.g. `onoutroend={...}`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the transition: page: bidirectional behaviour, local by default and |global, parameters, Web Animations accessibility note with prefersReducedMotion, and the four intro/outro events. Nothing removed.
