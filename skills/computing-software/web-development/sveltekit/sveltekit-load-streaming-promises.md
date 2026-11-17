---
id: computing-software.web-development.sveltekit.sveltekit-load-streaming-promises
name: sveltekit-load-streaming-promises
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, load, streaming, promises, server-load, skeleton, await]
level: practitioner
status: docs-checked
description: "Stream slow non-essential data from a SvelteKit server load by returning promises, and avoid unhandled rejections."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/20-load.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: render the page before slow data arrives.

Server `load` functions stream returned promises to the browser as they resolve. Put the `await` last so slow items start in parallel:

```js
// src/routes/blog/[slug]/+page.server.js
export async function load({ params }) {
	return {
		// make sure the `await` happens at the end, otherwise we
		// can't start loading comments until we've loaded the post
		comments: loadComments(params.slug),
		post: await loadPost(params.slug)
	};
}
```

```svelte
{#await data.comments}
	Loading comments...
{:then comments}
	{#each comments as comment}<p>{comment.content}</p>{/each}
{:catch error}
	<p>error loading comments: {error.message}</p>
{/await}
```

## Handle rejections
The server could crash with an "unhandled promise rejection" error if a lazy promise fails before rendering starts and nothing handles it. SvelteKit's own `fetch` is handled for you. For other promises, a noop catch marks them handled:

```js
const ok_manual = Promise.reject();
ok_manual.catch(() => {});
return {
	ok_manual,
	ok_fetch: fetch('/fetch/that/could/fail'),
	dangerous_unhandled: Promise.reject()
};
```

## Gotchas (from the page)
- Platforms without streaming (AWS Lambda, Firebase) buffer: the page renders only after all promises resolve. Make sure proxies such as NGINX do not buffer responses.
- Streaming needs JavaScript. Do not return promises from a universal `load` on a server-rendered page: they are not streamed, the promise is recreated when the function reruns in the browser.
- Headers and status cannot change once streaming starts: no `setHeaders` or redirects inside a streamed promise.
- In SvelteKit 1.x top-level promises were awaited automatically and only nested promises streamed.
- Independent `load` functions already run concurrently; during client navigation the results of multiple server loads are grouped into one response, and the page renders once all have returned.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `20-core-concepts/20-load.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
