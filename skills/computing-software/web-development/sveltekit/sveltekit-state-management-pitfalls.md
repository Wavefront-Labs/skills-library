---
id: computing-software.web-development.sveltekit.sveltekit-state-management-pitfalls
name: sveltekit-state-management-pitfalls
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, state-management, context, shared-state, ssr, reactivity, url-state]
level: intro
status: docs-checked
description: "Avoid shared server state and load side-effects in SvelteKit, use context for app state, make page values reactive, and keep state in the URL."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/50-state-management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep state correct across a server that serves many users and a client that reuses components.

## Never share state on the server
Servers are long-lived and shared. A module-level variable written from an action or load (`let user;` assigned in `actions.default`) is visible to every visitor, and lost on restart. Authenticate with `cookies` and persist to a database instead.

## No side-effects in load
Keep `load` pure (a `console.log` is fine). Do not write to a global store inside it (`user.set(await response.json())` is the page's "NEVER DO THIS"). Return the data and pass it down, or read `page.data`:
```js
export async function load({ fetch }) {
	const response = await fetch('/api/user');
	return { user: await response.json() };
}
```
Without SSR there is no cross-user leak, but side-effect-free loads are still easier to reason about.

## Use context for app state
`page.data` and other app state work on the server because they use Svelte context. Do the same:
```svelte
<!-- src/routes/+layout.svelte -->
<script>
	import { setContext } from 'svelte';
	let { data } = $props();
	// pass a function so reactivity survives crossing boundaries
	setContext('user', () => data.user);
</script>
```
```svelte
<!-- src/routes/user/+page.svelte -->
<script>
	import { getContext } from 'svelte';
	const user = getContext('user');
</script>
<p>Welcome {user().name}</p>
```
During SSR, updating context state deeper in the tree does not affect parents (already rendered); on the client it does propagate. To avoid flashing on hydration, pass state down, not up. With no SSR now or ever, a shared module is safe.

## Component state is preserved on navigation
Navigating `/blog/my-short-post` to `/blog/my-long-post` reuses components: `data` updates, but `onMount`/`onDestroy` do not rerun and plain `const` values are not recomputed. Make derived values reactive:
```js
let wordCount = $derived(data.content.split(' ').length);
let estimatedReadingTime = $derived(wordCount / 250);
```
Use `afterNavigate` / `beforeNavigate` for logic that must rerun. To force a remount, wrap in `{#key page.url.pathname}...{/key}` (`page` from `$app/state`).

## URL and snapshots
State that should survive reload or affect SSR (filters, sorting) belongs in search params like `?sort=price&order=ascending`: set via `<a href>`, `<form action>` or `goto('?key=value')`; read via `url` in `load` or `page.url.searchParams` in components. Disposable UI state that should survive back-navigation fits snapshots.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 20-core-concepts/50-state-management.md in full. No claims trimmed.
