---
id: computing-software.web-development.svelte.snippet-basics
name: snippet-basics
category: computing-software
field: web-development
product: svelte
tags: [snippet-block, reusable-markup, snippet-scope, recursive-snippet, snippet-parameters]
level: practitioner
status: docs-checked
description: "Declare reusable markup chunks with {#snippet}: parameters and defaults, lexical scope, self-reference, and how snippets replace duplicated template code."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/06-snippet.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Snippets and render tags create reusable chunks of markup inside a component:

```svelte
{#snippet figure(image)}
  <figure>
    <img src={image.src} alt={image.caption} width={image.width} height={image.height} />
    <figcaption>{image.caption}</figcaption>
  </figure>
{/snippet}

{#each images as image}
  {#if image.href}
    <a href={image.href}>{@render figure(image)}</a>
  {:else}
    {@render figure(image)}
  {/if}
{/each}
```

Parameters: any number, with default values, and each may be destructured. Rest parameters are not allowed.

Scope: snippets can sit anywhere in the component and reference values from `<script>` or `{#each}` blocks. They are visible to everything in the same lexical scope (siblings and their children). A snippet `y` declared inside snippet `x` is not visible outside `x`; rendering it there errors.

Snippets can reference themselves and each other:

```svelte
{#snippet countdown(n)}
  {#if n > 0}
    <span>{n}...</span>
    {@render countdown(n - 1)}
  {:else}
    {@render blastoff()}
  {/if}
{/snippet}
```

Svelte 4 slots are deprecated in Svelte 5; snippets are more powerful and flexible. `createRawSnippet` builds snippets programmatically (advanced).

## Checked

2026-11-08. Read the {#snippet} page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
