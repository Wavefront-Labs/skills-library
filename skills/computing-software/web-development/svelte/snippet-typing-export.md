---
id: computing-software.web-development.svelte.snippet-typing-export
name: snippet-typing-export
category: computing-software
field: web-development
product: svelte
tags: [snippet-type, generics-attribute, export-snippet, script-module, typed-snippets]
level: advanced
status: docs-checked
description: "Type Svelte snippet props with Snippet tuples and generics, and export top-level snippets from script module (Svelte 5.5+) for reuse across components."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/06-snippet.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Snippets implement the `Snippet` interface from `'svelte'`. The type argument is a tuple because snippets may have several parameters.

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    data: any[];
    children: Snippet;
    row: Snippet<[any]>;
  }

  let { data, children, row }: Props = $props();
</script>
```

Tie `data` and `row` to the same type with a generic:

```svelte
<script lang="ts" generics="T">
  import type { Snippet } from 'svelte';

  let { data, children, row }: {
    data: T[];
    children: Snippet;
    row: Snippet<[T]>;
  } = $props();
</script>
```

Exporting: top-level snippets of a `.svelte` file can be exported from `<script module>` for other components, provided they do not reference declarations in the non-module `<script>` (directly or through other snippets). Requires Svelte 5.5.0 or newer.

```svelte
<!-- snippets.svelte -->
<script module>
  export { add };
</script>

{#snippet add(a, b)}
  {a} + {b} = {a + b}
{/snippet}
```

Use it with `import { add } from './snippets.svelte';` then `{@render add(1, 2)}`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte snippet docs page (Typing snippets and Exporting snippets sections): `Snippet` tuple type, `generics="T"` example, export from `<script module>` and its restriction, and the 5.5.0 requirement. Nothing removed.
