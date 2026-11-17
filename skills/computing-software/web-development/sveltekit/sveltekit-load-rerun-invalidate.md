---
id: computing-software.web-development.sveltekit.sveltekit-load-rerun-invalidate
name: sveltekit-load-rerun-invalidate
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, load, invalidate, depends, untrack, refresh-all, dependency-tracking, rerun]
level: practitioner
status: docs-checked
description: "Predict when SvelteKit load functions rerun and force or prevent reruns with depends, invalidate, refreshAll and untrack."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/20-load.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control when `load` reruns.

SvelteKit tracks what each `load` reads. A load reruns when:
- a property of `params` it references changed;
- a property of `url` it references changed (`url.pathname`, `url.search`, ...); properties of `request.url` are not tracked;
- it calls `url.searchParams.get/getAll/has` and that parameter changed (other `searchParams` access behaves like `url.search`). Search params are tracked independently: `?x=1` to `?x=2` reruns a load reading `x`, `?x=1&y=1` to `?x=1&y=2` does not;
- it calls `await parent()` and a parent load reran; also a child server load that calls `await parent()` reruns when it is rerunning and the parent is also a server load (a universal load that calls `await parent()` reuses the parent's existing data instead);
- it declared a dependency via `fetch(url)` (universal only) or `depends(url)` and that URL was invalidated with `invalidate(url)`;
- `refreshAll()` was called.

Tracking does not apply after `load` returns: reading `params.x` inside a nested promise will not rerun it (dev shows a warning). Read it in the main body.

## Untrack
```js
export async function load({ untrack, url }) {
	// Untrack url.pathname so that path changes don't trigger a rerun
	if (untrack(() => url.pathname === '/')) {
		return { message: 'Welcome!' };
	}
}
```

## Manual invalidation
```js
// +page.js
export async function load({ fetch, depends }) {
	// reruns when invalidate('https://api.example.com/random-number') is called...
	const response = await fetch('https://api.example.com/random-number');
	// ...or when invalidate('app:random') is called
	depends('app:random');
	return { number: await response.json() };
}
```
```js
import { invalidate, refreshAll } from '$app/navigation';

invalidate('app:random');
invalidate('https://api.example.com/random-number');
invalidate((url) => url.href.includes('random-number'));
refreshAll();
```
Custom identifiers must start with `[a-z]:`. `refreshAll()` reruns every load and all active queries; unlike the deprecated `invalidateAll`, it does not reset `page.state`. Server loads never automatically depend on a fetched URL, to avoid leaking secrets to the client.

## Component state
A rerun updates the `data` prop in `+layout.svelte` / `+page.svelte`; the component is not recreated, so internal state persists. To reset, use an `afterNavigate` callback and/or wrap the component in a `{#key ...}` block.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/20-load.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
