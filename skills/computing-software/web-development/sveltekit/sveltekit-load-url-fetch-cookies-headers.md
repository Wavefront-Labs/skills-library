---
id: computing-software.web-development.sveltekit.sveltekit-load-url-fetch-cookies-headers
name: sveltekit-load-url-fetch-cookies-headers
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, load, load-fetch, cookies, set-headers, url, params, route]
level: intro
status: docs-checked
description: "Use url, route, params, the load fetch, cookies and setHeaders correctly inside SvelteKit load functions."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/20-load.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: read request info and make credentialed, cache-aware requests from `load`.

## url, route, params
- `url` is a `URL`; use `url.searchParams` for the query. `url.hash` cannot be accessed during `load` (it is unavailable on the server). Behind some adapters (e.g. adapter-node) you may need to configure the adapter so the URL is right.
- `route.id` is the route directory relative to `src/routes`, e.g. `'/a/[b]/[...c]'`.
- `params` derives from `url.pathname` and `route.id`: id `/a/[b]/[...c]` with path `/a/x/y/z` gives `{ "b": "x", "c": "y/z" }`.

## fetch
The `fetch` passed to `load` acts like native fetch plus:
- on the server it inherits the page request's `cookie` and `authorization` headers (credentialed requests);
- relative URLs work on the server;
- requests to `+server.js` routes call the handler directly, with no HTTP call;
- during SSR the response is inlined into the HTML via the `text`, `json` and `arrayBuffer` methods; headers are not serialized unless listed in `filterSerializedResponseHeaders` (hook `handle`);
- during hydration the response is read from the HTML, avoiding a second request (this is why the browser warns if you use global `fetch` in `load`).

```js
export async function load({ fetch, params }) {
	const res = await fetch(`/api/items/${params.id}`);
	return { item: await res.json() };
}
```

## Cookies (server load)
```js
export async function load({ cookies }) {
	const sessionid = cookies.get('sessionid');
	return { user: await db.getUser(sessionid) };
}
```
Defaults for `httpOnly`, `secure` and `path` are provided when setting cookies. Cookies are forwarded by `fetch` only to the app's own host or a more specific subdomain: when serving my.domain.com, `my.domain.com` and `sub.my.domain.com` receive them; `domain.com` and `api.domain.com` do not. With `credentials: 'include'` other cookies are not passed; work around it with the `handleFetch` hook.

## setHeaders
Available in server and universal `load`; only has an effect on the server.
```js
export async function load({ fetch, setHeaders }) {
	const response = await fetch('https://cms.example.com/products.json');
	setHeaders({
		age: response.headers.get('age'),
		'cache-control': response.headers.get('cache-control')
	});
	return response.json();
}
```
Setting the same header more than once (even across different `load` functions) is an error. A `set-cookie` header cannot be added this way; use `cookies.set(name, value, options)`.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/20-load.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
