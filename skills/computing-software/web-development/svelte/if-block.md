---
id: computing-software.web-development.svelte.if-block
name: if-block
category: computing-software
field: web-development
product: svelte
tags: [if-block, conditional-rendering, else-if, template-if, svelte-blocks]
level: intro
status: docs-checked
description: "Render content conditionally in Svelte with {#if}, {:else if} and {:else} blocks, which can wrap elements or plain text."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/02-if.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap conditionally rendered content in an if block:

```svelte
{#if answer === 42}
  <p>what was the question?</p>
{/if}
```

Add conditions with `{:else if expression}`, optionally ending in `{:else}`:

```svelte
{#if porridge.temperature > 100}
  <p>too hot!</p>
{:else if 80 > porridge.temperature}
  <p>too cold!</p>
{:else}
  <p>just right!</p>
{/if}
```

Forms:
- `{#if expression}...{/if}`
- `{#if expression}...{:else if expression}...{/if}`
- `{#if expression}...{:else}...{/if}`

Blocks do not have to wrap elements; they can also wrap text within elements.

## Checked

2026-11-08. Read the {#if} page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
