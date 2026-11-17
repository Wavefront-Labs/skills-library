---
id: computing-software.web-development.sveltekit.sveltekit-handle-hook
name: sveltekit-handle-hook
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, hooks, handle, locals, resolve, transformpagechunk, preload]
level: practitioner
status: docs-checked
description: "Write a SvelteKit handle hook in src/hooks.server.js to intercept requests, populate event.locals, and tune rendering through resolve options."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/20-hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit handle hook

Goal: run code on every server request, attach per-request data, and control how the response is rendered.

## Where it lives

Hooks files are all optional: `src/hooks.server.js` (server), `src/hooks.client.js` (client), `src/hooks.js` (both). `handle` goes in `src/hooks.server.js`. It runs for every request, including during prerendering, but not for static assets (including already-prerendered pages). If unimplemented it defaults to `({ event, resolve }) => resolve(event)`.

## Basic shape

```js
/** @type {import('@sveltejs/kit/hooks').Handle} */
export async function handle({ event, resolve }) {
	if (event.url.pathname.startsWith('/custom')) {
		return new Response('custom response');
	}

	const response = await resolve(event);
	return response;
}
```

Returning your own `Response` bypasses SvelteKit entirely. `resolve(...)` never throws; it always returns a `Promise<Response>` with the right status. An error thrown elsewhere in `handle` is fatal: SvelteKit answers with JSON or the fallback error page (customisable via `src/error.html`) depending on the `Accept` header.

## Passing data with locals

Populate `event.locals` and it is available in `+server.js` handlers and server `load` functions:

```js
export async function handle({ event, resolve }) {
	event.locals.user = await getUserInformation(event.cookies.get('sessionid'));
	const response = await resolve(event);
	response.headers.set('x-custom-header', 'potato');
	return response;
}
```

Type the data by augmenting `App.Locals` in `src/app.d.ts`. Modifying response headers is not always safe: some `Response` objects have immutable headers (for example `Response.redirect()` returned from an endpoint) and setting them throws a `TypeError`. Clone the response or avoid creating one with immutable headers.

## resolve options

The optional second argument can have:

- `transformPageChunk({ html, done })` - transform the HTML. Chunks may be partial (an opening tag without its closing tag) but split at sensible boundaries.
- `filterSerializedResponseHeaders(name, value)` - which headers to include in serialized responses when `load` uses `fetch`. By default none are included.
- `preload({ type, path })` - decide which files get preloaded (`type` is `'js'`, `'css'`, `'asset'`, or `'font'` which also carries `filename`). JS and CSS are preloaded by default. Not called in dev mode.

```js
const response = await resolve(event, {
	transformPageChunk: ({ html }) => html.replace('old', 'new'),
	filterSerializedResponseHeaders: (name) => name.startsWith('x-'),
	preload: ({ type, path }) => type === 'js' || path.includes('/important/')
});
```

## Gotchas

- To skip code during prerendering, check that the app is not `building`.
- Combine several `handle` functions with the `sequence` helper from `@sveltejs/kit/hooks`.
- For remote function requests, `route`, `params` and `url` describe the page that called the function, not the endpoint. Never use them for authorization decisions, since they come from a request that could be manipulated.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `30-advanced/20-hooks.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: the module attribution for `building` in the Gotchas bullet (the page only links it, so the bullet states what the sentence says).

Method: documentation only; no commands were run.
