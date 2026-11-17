---
id: computing-software.web-development.svelte.each-block
name: each-block
category: computing-software
field: web-development
product: svelte
tags: [each-block, keyed-each, list-rendering, each-else, destructuring-each]
level: practitioner
status: docs-checked
description: "Svelte {#each} blocks: iterable inputs, index, keyed blocks for stable identity, destructuring, repeating n times without an item, and the empty-list else clause."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/03-each.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Values may be arrays, array-like objects (anything with `length`), or iterables like `Map` and `Set` (converted with `Array.from`). `null` or `undefined` is treated as an empty array.

```svelte
{#each items as item, i}
  <li>{i + 1}: {item.name} x {item.qty}</li>
{/each}
```

Keyed: a key expression that uniquely identifies each item lets Svelte insert, move and delete items instead of changing the end and updating the middle. Strings and numbers are recommended keys so identity persists when objects change.

```svelte
{#each items as item, i (item.id)}
  <li>{i + 1}: {item.name} x {item.qty}</li>
{/each}
```

Destructuring and rest patterns work: `{#each items as { id, name, qty }, i (id)}`, `{#each objects as { id, ...rest }}`, `{#each items as [id, ...rest]}`.

No item: repeat n times by omitting `as`: `{#each { length: 8 }, rank}...{/each}`.

Else: `{:else}` renders when the list is empty.

```svelte
{#each todos as todo}
  <p>{todo.text}</p>
{:else}
  <p>No tasks today!</p>
{/each}
```

## Checked

Method: docs-only read of cited pages, 2026-11-08
