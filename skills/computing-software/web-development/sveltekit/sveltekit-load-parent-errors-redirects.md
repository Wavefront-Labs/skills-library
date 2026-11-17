---
id: computing-software.web-development.sveltekit.sveltekit-load-parent-errors-redirects
name: sveltekit-load-parent-errors-redirects
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, load, parent, error, redirect, auth, get-request-event, waterfall]
level: practitioner
status: docs-checked
description: "Use await parent(), error(), redirect() and getRequestEvent in SvelteKit load functions, and place auth checks so they actually run."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/20-load.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: share data between load functions, stop execution with errors or redirects, and guard routes.

## Parent data
`const { a } = await parent();` returns merged data from all parent loads (not only the immediate parent).
- In `+page.server.js` / `+layout.server.js`, `parent` returns data from parent `+layout.server.js` files.
- In `+page.js` / `+layout.js` it returns parent `+layout.js` data; a missing `+layout.js` acts like `({ data }) => data`, so unshadowed `+layout.server.js` data is included too.
- Avoid waterfalls: start independent work first and call `await parent()` after it.

```js
export async function load({ params, parent }) {
	const data = await getData(params);
	const parentData = await parent();
	return { ...data, meta: { ...parentData.meta, ...data.meta } };
}
```

## Errors
Import `error` from `@sveltejs/kit`; it throws, so it works inside helper functions. The nearest `+error.svelte` renders. Every error goes to the `handleError` hook; an unknown error is a 500 unless the hook says otherwise.
```js
if (!locals.user) error(401, 'not logged in');
if (!locals.user.isAdmin) error(403, 'not an admin');
```
(In SvelteKit 1.x you had to `throw` it yourself.)

## Redirects
`redirect(307, '/login')` from `@sveltejs/kit` also throws. Do not call it inside a `try {...}` block: the catch would trigger immediately. In the browser, outside `load`, navigate with `goto` from `$app/navigation`.

## Auth implications
- Layout `load` functions do not run on every request (for example during client-side navigation between child routes).
- Layout and page loads run concurrently unless `await parent()` is called. If a layout load throws, the page load still runs but the client does not receive its data.
- Prefer `hooks` to protect many routes before any load runs, or guards directly in `+page.server.js` loads. A guard in `+layout.server.js` requires every child page to `await parent()` before protected code.

## getRequestEvent
In server loads, `getRequestEvent()` from `$app/server` returns the current event, so shared helpers need no arguments:
```js
import { redirect } from '@sveltejs/kit';
import { getRequestEvent } from '$app/server';

export function requireLogin() {
	const { locals, url } = getRequestEvent();
	if (!locals.user) {
		const params = new URLSearchParams({ redirectTo: url.pathname + url.search });
		redirect(303, `/login?${params}`);
	}
	return locals.user;
}
```
Call `requireLogin()` at the top of any `load` (or form action).

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/20-load.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
