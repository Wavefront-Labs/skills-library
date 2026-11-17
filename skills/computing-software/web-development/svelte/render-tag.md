---
id: computing-software.web-development.svelte.render-tag
name: render-tag
category: computing-software
field: web-development
product: svelte
tags: [render-tag, at-render, render-snippet, optional-chaining-render, dynamic-snippet]
level: intro
status: docs-checked
description: "Render a snippet with {@render}: identifier or arbitrary expression, choosing between snippets, and optional snippets via optional chaining or an if block."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/07-%40render.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `{@render ...}` to render a snippet:

```svelte
{#snippet sum(a, b)}
  <p>{a} + {b} = {a + b}</p>
{/snippet}

{@render sum(1, 2)}
{@render sum(3, 4)}
```

The expression can be an identifier like `sum` or any JavaScript expression:

```svelte
{@render (cool ? coolSnippet : lameSnippet)()}
```

Optional snippets: if the snippet may be undefined (for example an incoming prop), use optional chaining so it renders only when defined:

```svelte
{@render children?.()}
```

Or use an `{#if}` block with `:else` for fallback content:

```svelte
{#if children}
  {@render children()}
{:else}
  <p>fallback content</p>
{/if}
```

See `snippet-basics` for declaring snippets.

## Checked

2026-11-08. Read the {@render} page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
