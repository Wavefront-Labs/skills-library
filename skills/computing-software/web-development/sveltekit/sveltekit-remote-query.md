---
id: computing-software.web-development.sveltekit.sveltekit-remote-query
name: sveltekit-remote-query
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-query, query, await, svelte]
level: practitioner
status: docs-checked
description: "Define a SvelteKit remote query, consume it with await or loading/error/current, and rely on argument caching, deduplication and refresh()."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: read dynamic server data from components with `query` from `$app/server`.

```js
// src/routes/blog/data.remote.js
import { query } from '$app/server';
import * as db from '#lib/server/database.js';

export const getPosts = query(async () => {
	return await db.sql`SELECT title, slug FROM post ORDER BY published_at DESC`;
});
```

```svelte
<script>
	import { getPosts } from './data.remote';
</script>
{#each await getPosts() as { title, slug }}
	<li><a href="/blog/{slug}">{title}</a></li>
{/each}
```

Until the promise resolves, or if it errors, the nearest `<svelte:boundary>` is invoked. Alternative without `await`: `const query = getPosts();` then use `query.error`, `query.loading` and `query.current`.

## Arguments

```js
export const getPost = query(v.string(), async (slug) => {
	const [post] = await db.sql`SELECT * FROM post WHERE slug = ${slug}`;
	if (!post) error(404, 'Not found');
	return post;
});
```

Consume with `const post = $derived(await getPost(params.slug));`. Arguments and return values are serialized with devalue (handles `Date`, `Map`, and types from your transport hook). For `query` and `prerender` arguments (not return values), objects, maps and sets are sorted so equal members give the same cache key; `getPosts({ limit: 10, offset: 10 })` equals `getPosts({ offset: 10, limit: 10 })`. Use an array if order matters.

## Deduplication

The serialized argument is the cache key. On the server this makes a request-scoped cache; on the client identical calls point to the same instance. You can `await` a query in components, event handlers, universal `load` functions and async callbacks and it dedupes. The cache lives while the query is in use and is released afterwards.

## Refreshing

`getPosts().refresh()` re-fetches the latest value. Because `getPosts() === getPosts()` while on the page, you do not need to hold a reference.

## Gotcha

Queries cannot be used when the whole page is prerendered (`export const prerender = true` on the page or a parent layout, e.g. `adapter-static`). For static data use `prerender` functions.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block), query section. One fix: the import path in the example is now #lib/server/database.js, matching the page and the v3 convention.
