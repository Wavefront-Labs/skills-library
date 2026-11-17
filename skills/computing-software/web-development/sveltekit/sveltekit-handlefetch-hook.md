---
id: computing-software.web-development.sveltekit.sveltekit-handlefetch-hook
name: sveltekit-handlefetch-hook
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, hooks, handlefetch, fetch, cookies, credentials, subdomain]
level: practitioner
status: docs-checked
description: "Use the SvelteKit handleFetch hook to rewrite server-side event.fetch requests, such as hitting an API directly during SSR or forwarding cookies to a sibling subdomain."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/20-hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit handleFetch hook

Goal: modify or replace the result of `event.fetch` calls made on the server.

`handleFetch` goes in `src/hooks.server.js`. It applies to `event.fetch` calls that run on the server (or during prerendering) inside an endpoint, `load`, `action`, `handle`, `handleError` or `reroute`.

## Use case: bypass the public network during SSR

A `load` function may call a public URL such as `https://api.yourapp.com` on client-side navigation, but during SSR it can hit the API directly, skipping proxies and load balancers:

```js
/** @type {import('@sveltejs/kit/hooks').HandleFetch} */
export async function handleFetch({ request, fetch }) {
	if (request.url.startsWith('https://api.yourapp.com/')) {
		// clone the original request, but change the URL
		request = new Request(
			request.url.replace('https://api.yourapp.com/', 'http://localhost:9999/'),
			request
		);
	}

	return fetch(request);
}
```

## Credentials model

`event.fetch` follows the browser's credentials model:

- Same-origin: `cookie` and `authorization` headers are forwarded unless `credentials` is `"omit"`.
- Cross-origin: `cookie` is included if the request URL belongs to a subdomain of the app (app on `my-domain.com`, API on `api.my-domain.com`).

## Sibling subdomain caveat

If app and API are on sibling subdomains (`www.my-domain.com` and `api.my-domain.com`), a cookie belonging to the common parent domain `my-domain.com` is not included, because SvelteKit cannot know which domain the cookie belongs to. Copy it manually:

```js
export async function handleFetch({ event, request, fetch }) {
	if (request.url.startsWith('https://api.my-domain.com/')) {
		request.headers.set('cookie', event.request.headers.get('cookie'));
	}

	return fetch(request);
}
```

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `30-advanced/20-hooks.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
