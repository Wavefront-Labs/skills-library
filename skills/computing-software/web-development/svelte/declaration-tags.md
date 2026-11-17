---
id: computing-software.web-development.svelte.declaration-tags
name: declaration-tags
category: computing-software
field: web-development
product: svelte
tags: [declaration-tags, local-const, at-const, reactive-local-state, lexical-scope]
level: practitioner
status: docs-checked
description: "Define local variables in Svelte markup with {const} and {let} declaration tags (5.56+), reactive with $state and $derived, versus the legacy {@const} tag."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/11-declaration-tags.md
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/10-%40const.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Declaration tags define local variables inside markup, available since Svelte 5.56:

```svelte
{#each boxes as box}
  {const area = box.width * box.height}
  {const label = `${box.width} x ${box.height} = ${area}`}
  <p>{label}</p>
{/each}
```

Reactive values use `$state` and `$derived`:

```svelte
{#if editing}
  {let name = $state(user.name)}
  {const greeting = $derived(`Hello ${name}`)}
  <input bind:value={name} />
  <p>{greeting}</p>
{/if}
```

They work anywhere in the component, may reference `<script>` values and `{#each}` variables, and are visible to siblings and their children. An inner tag can shadow an outer one (`{const hello = 'hi'}` inside a `<div>`), and the outer value returns after the element.

Legacy: `{@const x = y}` is considered legacy; use `{const x = $derived(y)}`. `{@const}` is only allowed as an immediate child of a block (`{#if}`, `{#each}`, `{#snippet}` and so on), a `<Component />` or a `<svelte:boundary>`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the declaration tags and {@const} pages: const/let tags since 5.56, $state/$derived use, lexical scope and shadowing, and the legacy {@const} placement rule. Nothing removed.
