---
id: computing-software.web-development.sveltekit.sveltekit-init-reroute-transport-hooks
name: sveltekit-init-reroute-transport-hooks
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, hooks, init, reroute, transport, i18n, serialization]
level: advanced
status: docs-checked
description: "Use the SvelteKit init, reroute and transport hooks for one-time startup work, URL-to-route translation, and passing custom class instances across the server/client boundary."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/20-hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit init, reroute and transport hooks

## init (src/hooks.server.js and src/hooks.client.js)

Runs once when the server is created or the app starts in the browser. Good for async setup such as opening a database connection:

```js
import * as db from '#lib/server/database.js';

/** @type {import('@sveltejs/kit/hooks').ServerInit} */
export async function init() {
	await db.connect();
}
```

With top-level await it is equivalent to top-level module code, but some environments (notably Safari) lack top-level await. In the browser, async work in `init` delays hydration, so keep it light.

## reroute (src/hooks.js, runs on server and client)

Runs before `handle`. The pathname it returns (default `url.pathname`) is used to select the route and its params. Example: serve `src/routes/[[lang]]/about/+page.svelte` at translated URLs:

```js
const translated = {
	'/en/about': '/en/about',
	'/de/ueber-uns': '/de/about',
	'/fr/a-propos': '/fr/about',
};

/** @type {import('@sveltejs/kit/hooks').Reroute} */
export function reroute({ url }) {
	if (url.pathname in translated) {
		return translated[url.pathname];
	}
}
```

The `lang` param is derived from the returned pathname. Rerouting does not change the address bar or `event.url`.

Since 2.18 `reroute` may be async, e.g. to ask your backend where to go. Use the provided `fetch` argument (same benefits as `load`'s fetch; `params` and `id` are unavailable to `handleFetch` because the route is not yet known). Keep it fast, or navigation is delayed. Guard against recursion, as the docs example does:

```js
export async function reroute({ url, fetch }) {
	if (url.pathname === '/api/reroute') return;

	const api = new URL('/api/reroute', url);
	api.searchParams.set('pathname', url.pathname);

	const result = await fetch(api).then(r => r.json());
	return result.pathname;
}
```

`reroute` must be pure and idempotent (same input, same output, no side effects); SvelteKit caches the result on the client per unique URL.

## transport (src/hooks.js)

Lets custom types returned from `load` and form actions cross the server/client boundary. Each transporter has `encode` (return a falsy value for anything that is not your type) and `decode`:

```js
import { Vector } from '#lib/math.js';

/** @type {import('@sveltejs/kit/hooks').Transport} */
export const transport = {
	Vector: {
		encode: (value) => value instanceof Vector && [value.x, value.y],
		decode: ([x, y]) => new Vector(x, y)
	}
};
```

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `30-advanced/20-hooks.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
