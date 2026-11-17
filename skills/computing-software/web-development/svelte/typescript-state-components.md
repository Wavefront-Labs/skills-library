---
id: computing-software.web-development.svelte.typescript-state-components
name: typescript-state-components
category: computing-software
field: web-development
product: svelte
tags: [typed-state, component-type, component-props-type, augment-svelte-elements, dom-type-enhancement]
level: advanced
status: docs-checked
description: "TypeScript with Svelte state and components: $state generics and casts, the Component and ComponentProps types, and augmenting svelte/elements for custom attributes."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/03-typescript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`$state`: `let count: number = $state(0);`. With no initial value the type includes `undefined`, so `let count: number = $state();` errors. Use the generic, `let count = $state<number>();` (inferred `number | undefined`), or cast when it will be defined before use, especially in classes:

```ts
class Counter {
  count = $state() as number;
  constructor(initial: number) { this.count = initial; }
}
```

`Component` type: restrict what can be passed to a dynamic component.

```svelte
<script lang="ts">
  import type { Component } from 'svelte';
  interface Props { DynamicComponent: Component<{ prop: string }>; }
  let { DynamicComponent }: Props = $props();
</script>
<DynamicComponent prop="foo" />
```

(Svelte 4 components were `SvelteComponent`.) `ComponentProps<TComponent>` extracts a component's props. For a constructor or instance: `let componentConstructor: typeof MyComponent = MyComponent;` and `let componentInstance: MyComponent;` with `bind:this`.

Enhancing DOM types: for custom or experimental attributes and events, augment `svelte/elements` in a `.d.ts`:

```ts
import { HTMLButtonAttributes } from 'svelte/elements';

declare module 'svelte/elements' {
  export interface SvelteHTMLElements { 'custom-button': HTMLButtonAttributes; }
  export interface HTMLAttributes<T> { globalattribute?: string; }
  export interface HTMLButtonAttributes { veryexperimentalattribute?: string; }
}
export {}; // keep it a module so types are augmented, not overridden
```

Make sure `tsconfig.json` includes the file; reload if needed.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte TypeScript page: $state typing, generic and as-cast forms, the Component and ComponentProps types, typeof/instance typing and the svelte/elements augmentation example. Nothing removed.
