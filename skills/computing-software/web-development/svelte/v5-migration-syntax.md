---
id: computing-software.web-development.svelte.v5-migration-syntax
name: v5-migration-syntax
category: computing-software
field: web-development
product: svelte
tags: [svelte-5-migration, migrate-script, let-to-state, export-let-to-props, slots-to-snippets, callback-props]
level: practitioner
status: docs-checked
description: "Migrate Svelte 4 syntax to Svelte 5: let to $state, $: to $derived or $effect, export let to $props, on: to onclick, createEventDispatcher to callback props, slots to snippets."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/07-v5-migration-guide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Svelte 5 still supports Svelte 4 syntax and you can mix components. Run `npx sv migrate svelte-5` to bump dependencies and convert most syntax automatically.

Mappings:
- `let count = 0` becomes `let count = $state(0)`.
- `$: double = count * 2` becomes `const double = $derived(count * 2)`. A `$:` side effect becomes `$effect(() => {...})`, which runs at different times than `$:`.
- `export let optional = 'unset'; export let required;` becomes `let { optional = 'unset', required } = $props();`. Rename with `let { class: klass } = $props()`. Replace `$$restProps` with `...rest`, and `$$props` with `let props = $props()`.
- `on:click={...}` becomes `onclick={...}`; shorthand `{onclick}` works.
- `createEventDispatcher` is deprecated: accept callback props (`let { inflate } = $props()`, call `inflate(power)`, no `.detail`). Forward events by accepting `onclick` and spreading `{...props}`.
- Event modifiers do not work on attributes. Call `event.preventDefault()` in the handler; `capture` becomes `onclickcapture`. Duplicate handlers are not allowed, so call both from one function; with spreads, put local handlers after the spread.
- `<slot />` becomes `{@render children?.()}`; named slots become snippet props; `let:` data becomes snippet parameters.

Not auto-migrated: `createEventDispatcher` and `beforeUpdate`/`afterUpdate` (often `$effect.pre` plus `tick`). Uncertain `$:` statements become `run` from `svelte/legacy`; prefer `$derived`.

See `v5-migration-components-breaking` for API and breaking changes.

## Checked

Method: docs-only read of cited pages, 2026-11-08
