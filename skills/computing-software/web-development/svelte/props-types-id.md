---
id: computing-software.web-development.svelte.props-types-id
name: props-types-id
category: computing-software
field: web-development
product: svelte
tags: [props-typing, props-id, unique-id, aria-labelledby, snippet-type]
level: practitioner
status: docs-checked
description: "Type $props with TypeScript or JSDoc, and use $props.id() (5.20+) for per-instance IDs that stay stable between server render and hydration."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/05-%24props.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Type props by annotating the declaration.

TypeScript:

```svelte
<script lang="ts">
  interface Props { adjective: string }
  let { adjective }: Props = $props();
</script>
```

JSDoc:

```svelte
<script>
  /** @type {{ adjective: string }} */
  let { adjective } = $props();
</script>
```

Interfaces for native DOM elements are in `svelte/elements`. Snippet props such as `children` are typed with `Snippet` imported from `'svelte'`. Typing is recommended so users can discover which props to supply.

`$props.id()`, added in 5.20.0: returns an ID unique to the current component instance. When hydrating a server-rendered component the value is consistent between server and client. Use it to link elements via `for` and `aria-labelledby`:

```svelte
<script>
  const uid = $props.id();
</script>
<label for="{uid}-firstname">First Name: </label>
<input id="{uid}-firstname" type="text" />
```

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte `$props` docs page (Type safety and `$props.id()` sections): TypeScript and JSDoc typing, `svelte/elements`, `Snippet` from `'svelte'`, `$props.id()` added in 5.20.0 and hydration consistency. Nothing removed.
