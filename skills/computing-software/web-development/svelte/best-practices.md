---
id: computing-software.web-development.svelte.best-practices
name: best-practices
category: computing-software
field: web-development
product: svelte
tags: [svelte-best-practices, runes-mode, avoid-legacy, keyed-each-index, styling-child-components]
level: practitioner
status: docs-checked
description: "Official Svelte best-practice checklist: when to use state, derived, effect and props, key blocks, keyed each, styling children, context, and legacy features to replace."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/01-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `$state` only for variables that cause an effect, derived or template update. Use `$state.raw` for large objects that are only reassigned (like API responses).
- Compute with `$derived` (expression) or `$derived.by` (function), not `$effect`. Deriveds are writable; objects returned are not deeply reactive.
- Effects are an escape hatch and should avoid updating state. Alternatives: `{@attach}` to sync external libraries, event handlers or function bindings for interaction, `$inspect` for logging, `createSubscriber` for external sources. Never wrap effect contents in `if (browser)`; effects do not run on the server.
- Treat props as changing: `let color = $derived(type === 'danger' ? 'red' : 'green')`.
- `$inspect.trace(label)` first line of an effect or `$derived.by` shows what triggered it.
- `{#key}` unmounts everything inside each time; use sparingly. Prefer `$derived` to re-run expressions.
- Use `onclick` attributes, `<svelte:window>`/`<svelte:document>` rather than `onMount` or `$effect` for listeners.
- Prefer keyed `{#each}`; the key must uniquely identify the item, never the index. Avoid destructuring if you mutate the item.
- JS variable into CSS: `style:--columns={columns}`. Style children via custom properties (`<Child --color="red" />`), else `div :global { h1 {...} }`.
- Prefer `createContext` over module state (no cross-user SSR leaks, type safe).
- Async: 5.36+ with `experimental.async`.
- Avoid legacy: `export let`, `$:`, `on:click`, `<slot>`, `<svelte:component>`, `<svelte:self>`, stores for shared reactivity, `use:action`, `class:`. Use `$props`, `$derived`, `onclick`, snippets, `{@attach}`, clsx-style `class`.

## Checked

2026-11-08: Read the Svelte best-practices page end to end (state, derived, effect, props, inspect.trace, key, events, each, CSS variables, child styling, context, async 5.36, legacy replacements). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
