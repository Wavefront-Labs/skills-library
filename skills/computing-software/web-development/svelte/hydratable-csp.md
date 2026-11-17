---
id: computing-software.web-development.svelte.hydratable-csp
name: hydratable-csp
category: computing-software
field: web-development
product: svelte
tags: [hydratable, hydration-data, devalue-serialization, csp-nonce, csp-hash]
level: sme
status: docs-checked
description: "Avoid redoing server async work during hydration with hydratable(key, fn): devalue serialization, library key prefixes, and CSP nonce or hash options for the inline script."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/05-hydratable.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Problem: awaiting data during server rendering means hydration on the client repeats the work and is blocked until it finishes. `hydratable` is a low-level API (usually used behind the scenes by data-fetching libraries, such as SvelteKit remote functions).

```svelte
<script>
  import { hydratable } from 'svelte';
  import { getUser } from 'my-database-library';

  const user = await hydratable('user', () => getUser());
</script>
<h1>{user.name}</h1>
```

On the server it serialises and stashes the result under the key in the `head` content. During hydration it returns the serialised version instead of running `getUser`. After hydration, calling it again invokes `getUser`.

It also gives random or time-based values that are stable across server and hydration: `hydratable('random', () => Math.random())`. Library authors should prefix keys with their library name to avoid conflicts.

Serialization: results must be serializable with `devalue`, which handles `Map`, `Set`, `URL`, `BigInt` and more; promises also work.

CSP: `hydratable` adds an inline `<script>` to the `head`. Pass `csp: { nonce }` to `render` (a fresh nonce per dynamically rendered response) and put the same nonce in `script-src 'nonce-...'`. For statically generated HTML use `csp: { hash: true }` and use the returned `hashes.script` array in the header. Prefer `nonce` since `hash` will interfere with future streaming SSR.

## Checked

2026-11-08: Read the Hydratable data page end to end (hydratable key and function, devalue types, library key prefix, nonce and hash CSP options, hashes.script, nonce preferred). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
