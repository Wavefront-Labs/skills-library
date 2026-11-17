---
id: computing-software.web-development.svelte.context-api
name: context-api
category: computing-software
field: web-development
product: svelte
tags: [create-context, set-context, get-context, prop-drilling, has-context]
level: practitioner
status: docs-checked
description: "Share values with descendants without prop drilling: createContext triplets (5.40+), setContext and getContext with keys, hasContext and getAllContexts."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/02-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Context lets components access values owned by parents without passing them as props through intermediate layers. It is especially useful when the parent renders the child via a `children` snippet and is unaware of it.

`createContext` (added in 5.40) returns a typed `[get, set, has]` triplet of functions; earlier versions must use `setContext`/`getContext`:

```ts
// context.ts
import { createContext } from 'svelte';

interface User { name: string }

export const [getUserContext, setUserContext] = createContext<User>();
```

Parent: `setUserContext({ name: 'world' });` in `<script>`. Child: `const user = getUserContext();`.

Without it, use keys:

```svelte
<script>
  import { setContext } from 'svelte';
  setContext('my-context', 'hello from Parent.svelte');
</script>
```

```svelte
<script>
  import { getContext } from 'svelte';
  const message = getContext('my-context');
</script>
```

The key and the value can be any JavaScript value. `createContext` is preferred: better type safety and no keys needed. Svelte also exposes `hasContext` and `getAllContexts`.

Reactive state in context: update the object (`counter.count = 0`) rather than reassigning it, or you break the link. Context is not shared between server requests, unlike state in a shared module that is mutated during SSR.

## Checked

2026-11-08: Read the Context page (createContext 5.40 triplet, setContext and getContext, hasContext and getAllContexts, state in context, SSR leak note). Corrected the createContext description from a pair to the page's [get, set, has] triplet and removed the unlocated sentence about setting context during initialisation.

Method: docs-only read of cited pages, 2026-11-08
