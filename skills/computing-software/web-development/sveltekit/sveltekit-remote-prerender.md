---
id: computing-software.web-development.sveltekit.sveltekit-remote-prerender
name: sveltekit-remote-prerender
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-prerender, prerender, static, build]
level: practitioner
status: docs-checked
description: "Use prerender remote functions to compute data at build time, set inputs and dynamic, and understand browser Cache API storage."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: serve data that changes at most once per deployment from build-time output.

`prerender` is like `query` but runs at build time:

```js
import { prerender } from '$app/server';

export const getPosts = prerender(async () => {
	return await db.sql`SELECT title, slug FROM post ORDER BY published_at DESC`;
});
```

It works on otherwise dynamic pages, giving partial prerendering: prerendered data can live on a CDN with your static assets, so navigation is fast. In the browser the data is stored with the `Cache` API; it survives reloads and is cleared when the user first visits a new deployment.

## Arguments

Validate with a Standard Schema as with queries:

```js
export const getPost = prerender(v.string(), async (slug) => {
	const [post] = await db.sql`SELECT * FROM post WHERE slug = ${slug}`;
	if (!post) error(404, 'Not found');
	return post;
});
```

Calls to `getPost(...)` found by the crawler while prerendering pages are saved automatically. Name values explicitly with `inputs`:

```js
export const getPost = prerender(
	v.string(),
	async (slug) => { /* ... */ },
	{
		inputs: () => ['first-post', 'second-post', 'third-post']
	}
);
```

## dynamic

By default prerender functions are excluded from the server bundle, so you cannot call them with arguments that were not prerendered. Set `dynamic: true` in the options object to keep them callable:

```js
{ dynamic: true, inputs: () => ['first-post', 'second-post', 'third-post'] }
```

## Notes

- Argument normalization (sorted objects, maps, sets) applies to `prerender` as it does to `query`; use an array if order matters.
- `redirect(...)` is allowed inside `prerender`.
- For data that must be fresh per request use `query`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block), prerender section: build-time behaviour, Cache API, dynamic option, input normalization. No claims trimmed.
