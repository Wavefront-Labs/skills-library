---
id: computing-software.web-development.svelte.key-block
name: key-block
category: computing-software
field: web-development
product: svelte
tags: [key-block, reinstantiate-component, replay-transition, template-key, destroy-recreate]
level: intro
status: docs-checked
description: "Use Svelte {#key} blocks to destroy and recreate content when an expression changes, reinitialising components or replaying transitions."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/04-key.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`{#key expression}...{/key}` destroys and recreates its contents whenever the expression's value changes.

Around a component, this reinstantiates and reinitialises it:

```svelte
{#key value}
  <Component />
{/key}
```

It is also useful to replay a transition whenever a value changes:

```svelte
{#key value}
  <div transition:fade>{value}</div>
{/key}
```

## Checked

2026-11-08. Read the {#key} page in full. Removed a comparison with keyed each blocks that the page does not make; the rest matched.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
