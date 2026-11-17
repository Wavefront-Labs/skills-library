---
id: computing-software.web-development.sveltekit.sveltekit-web-standards-apis
name: sveltekit-web-standards-apis
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, web-standards, fetch, request-response, formdata, url-searchparams, streams]
level: intro
status: docs-checked
description: "Use the standard Web APIs SvelteKit builds on: fetch, Request, Response, Headers, FormData, streams, URL, URLSearchParams and crypto."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/10-getting-started/40-web-standards.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse platform knowledge inside SvelteKit. These APIs exist in modern browsers and in Cloudflare Workers, Deno and Vercel Functions.

## fetch, Request, Response, Headers
- `fetch` works in hooks, server routes and the browser. A special `fetch` is passed to `load` functions, server hooks, API routes and remote functions: it calls endpoints directly during SSR without an HTTP call, keeps credentials, and allows relative URLs. Outside `load`, server-side credentialled fetches need explicit `cookie` and/or `authorization` headers.
- `event.request` (in hooks and server routes) offers `request.json()` and `request.formData()`.
- `+server.js` handlers return a `Response`; a SvelteKit app turns a `Request` into a `Response`.

```js
/// file: src/routes/what-is-my-user-agent/+server.js
export function GET({ request }) {
	console.log(...request.headers);
	return Response.json({
		userAgent: request.headers.get('user-agent')
	}, {
		headers: { 'x-custom-header': 'potato' }
	});
}
```

## FormData
```js
/// file: src/routes/hello/+server.js
export async function POST(event) {
	const body = await event.request.formData();
	console.log([...body]);
	return Response.json({ name: body.get('name') ?? 'world' });
}
```

## Streams
For responses too large for memory or sent in chunks use `ReadableStream`, `WritableStream`, `TransformStream`.

## URL
`event.url` (hooks, server routes), `page.url` (pages), `from`/`to` in `beforeNavigate`/`afterNavigate`. Query params: `url.searchParams.get('foo')`.

## Web Crypto
Available as the `crypto` global (used internally for CSP headers):
```js
const uuid = crypto.randomUUID();
```

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 10-getting-started/40-web-standards.md in full. No claims trimmed.
