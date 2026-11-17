---
id: computing-software.web-development.sveltekit.sveltekit-server-endpoints
name: sveltekit-server-endpoints
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, server-endpoints, server-js, api-routes, http-methods, content-negotiation, fallback-handler]
level: practitioner
status: docs-checked
description: "Write SvelteKit +server.js API endpoints: HTTP verb handlers, fallback handler, streaming, and how page versus endpoint requests are decided."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/10-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define a route with full control over the response using `+server.js`.

Export functions named for HTTP verbs (`GET`, `POST`, `PATCH`, `PUT`, `DELETE`, `OPTIONS`, `HEAD`, `QUERY`). Each takes a `RequestEvent` and returns a `Response`.

```js
/// file: src/routes/api/random-number/+server.js
import { error } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export function GET({ url }) {
	const min = Number(url.searchParams.get('min') ?? '0');
	const max = Number(url.searchParams.get('max') ?? '1');
	const d = max - min;

	if (isNaN(d) || d < 0) {
		error(400, 'min and max must be numbers, and min must be less than max');
	}

	return new Response(String(min + Math.random() * d));
}
```

## Receiving data
```js
/// file: src/routes/api/add/+server.js
/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	const { a, b } = await request.json();
	return Response.json(a + b);
}
```
Call it from a page with `fetch('/api/add', { method: 'POST', body: JSON.stringify({ a, b }), headers: { 'content-type': 'application/json' } })`. Form actions are generally the better way to submit browser data.

## Fallback
Export `fallback` to catch any unhandled method (including `MOVE`). For `HEAD`, `GET` takes precedence over `fallback`; a `HEAD` request to a route with `GET` returns the `content-length` of the GET body.
```js
export async function fallback({ request }) {
	return new Response(`I caught your ${request.method} request!`);
}
```

## Sharing a path with a page
- `PUT`/`PATCH`/`DELETE`/`OPTIONS`/`QUERY` always go to `+server.js`.
- `GET`/`POST`/`HEAD` go to the page if the `accept` header prioritises `text/html`, else to `+server.js`.
- `GET` responses carry `Vary: Accept`.

## Gotchas
- `error()` and `redirect()` from `@sveltejs/kit` are conveniences. Thrown errors give JSON or the `src/error.html` fallback depending on `Accept`; `+error.svelte` is not rendered.
- `Response` accepts a `ReadableStream` (streaming/SSE), except on platforms that buffer responses such as AWS Lambda.
- In dev Vite injects `Access-Control-Allow-Origin` and `Access-Control-Allow-Methods` for `OPTIONS`; they are absent in production unless you add them.
- `+layout` files do not affect `+server.js`; put per-request logic in the `handle` hook.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 20-core-concepts/10-routing.md in full, server section: verbs, fallback, HEAD and GET, content negotiation, streaming, OPTIONS. No claims trimmed.
