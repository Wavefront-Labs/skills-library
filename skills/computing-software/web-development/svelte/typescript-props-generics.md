---
id: computing-software.web-development.svelte.typescript-props-generics
name: typescript-props-generics
category: computing-software
field: web-development
product: svelte
tags: [typed-props, generics-script-attribute, html-button-attributes, svelte-html-elements, wrapper-component-types]
level: practitioner
status: docs-checked
description: "Type Svelte component props: Props interface with Snippet and rest index, the generics script attribute, and wrapper components using svelte/elements attribute types."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/03-typescript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Typing `$props`: like any object.

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    requiredProperty: number;
    optionalProperty?: boolean;
    snippetWithStringArgument: Snippet<[string]>;
    eventHandler: (arg: string) => void;
    [key: string]: unknown;
  }

  let { requiredProperty, optionalProperty, snippetWithStringArgument, eventHandler, ...everythingElse }: Props = $props();
</script>
```

Generics: relate props with the `generics` attribute, whose content is what you would put between `<...>` of a generic function (multiple generics, `extends` and fallback types allowed):

```svelte
<script lang="ts" generics="Item extends { text: string }">
  interface Props {
    items: Item[];
    select(item: Item): void;
  }
  let { items, select }: Props = $props();
</script>
```

Wrapper components expose all attributes of an element by using or extending `svelte/elements` interfaces:

```svelte
<script lang="ts">
  import type { HTMLButtonAttributes } from 'svelte/elements';
  let { children, ...rest }: HTMLButtonAttributes = $props();
</script>
<button {...rest}>{@render children?.()}</button>
```

For elements without a dedicated type, use `SvelteHTMLElements['div']`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte TypeScript page: Props interface with Snippet, the generics script attribute, HTMLButtonAttributes wrapper and SvelteHTMLElements fallback. Nothing removed.
