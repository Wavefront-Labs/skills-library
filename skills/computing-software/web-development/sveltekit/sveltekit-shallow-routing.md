---
id: computing-software.web-development.sveltekit.sveltekit-shallow-routing
name: sveltekit-shallow-routing
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, shallow-routing, page-state, goto, preload-data, modal, history]
level: advanced
status: docs-checked
description: "Create SvelteKit history entries with page.state and goto shallow: true for back-dismissable modals, including preloadData for route detail views."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/67-shallow-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add a history entry (e.g. a modal the back gesture dismisses) without a full navigation.

## Basic pattern
```svelte
<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import Modal from './Modal.svelte';

	function showModal() {
		goto('', { state: { showModal: true }, shallow: true });
	}
</script>

<button onclick={showModal}>open</button>

{#if page.state.showModal}
	<Modal close={() => history.back()} />
{/if}
```
`page.state` is global; type it by declaring `App.PageState` (usually in `src/app.d.ts`). Going back unsets it.

## Changing the URL bar
`goto('/another/page', { state, shallow: true })`. On reload the user lands on `/another/page`, not the rendered page. `beforeNavigate`, `onNavigate` and `afterNavigate` run with `navigation.type === 'goto'` and `navigation.shallow === true`.

While shallow, `page.shallow` is `{ url, params, route }` for the page that would render on reload; `page.url`, `page.params`, `page.route` still describe the rendered page. Example: `page.shallow?.url.href ?? page.url.href`. A regular `goto` without `shallow: true`, or a link click, exits shallow routing. Navigating back/forward to a shallow entry restores its `page.state` and `page.shallow`; to go to the visible URL call `goto(page.shallow.url)`.

In SvelteKit 2, `pushState` / `replaceState` did this; they are deprecated in favour of `goto` with `shallow: true` and the `replace` option.

## Options
- `replace: true`: replace the current history entry instead of adding one.
- `persistState: true`: restore the state after reload (default: not restored).
- `reset: true`: shallow navigations keep scroll position and focus by default; this opts out.

## Render another route's page
Use `preloadData(href)` in an `<a>` click handler, then:
```js
e.preventDefault();
const result = await preloadData(href);
if (result.type === 'loaded' && result.status === 200) {
	goto(href, { shallow: true, state: { selected: result.data } });
} else {
	goto(href); // something bad happened, navigate normally
}
```
Render `<PhotoPage data={page.state.selected} />` inside the modal when `page.state.selected` is set. Bail out of the handler for small screens and for `shiftKey`, `metaKey`, `ctrlKey` clicks. With `data-sveltekit-preload-data` on the element or a parent, `preloadData` reuses that request.

## Caveats
- Requires JavaScript; plan a fallback.
- `page.state` is only populated after JS loads (flicker risk) and is `{}` during SSR.
- After reload the browser goes straight to the previous `page.shallow.url`: `page.url.pathname` becomes `/photos/123` and `page.shallow` is `null`, regardless of `persistState` (initial load only).

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/67-shallow-routing.md in full: goto and state, App.PageState, page.shallow, persistState, preloadData, caveats. No claims trimmed.
