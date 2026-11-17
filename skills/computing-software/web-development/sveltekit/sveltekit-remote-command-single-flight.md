---
id: computing-software.web-development.sveltekit.sveltekit-remote-command-single-flight
name: sveltekit-remote-command-single-flight
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-command-single-flight, command, requested, mutations]
level: advanced
status: docs-checked
description: "Write data with a SvelteKit remote command and refresh queries in the same request using refresh(), set(), updates() and requested()."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: mutate data from anywhere and update stale queries in one round trip.

## command

`command` writes data like `form` but is not tied to an element. Prefer `form` where possible, since it degrades gracefully without JS. Validate any argument with a Standard Schema first:

```js
export const addLike = command(v.string(), async (id) => {
	await db.sql`UPDATE item SET likes = likes + 1 WHERE id = ${id}`;
});
```

Call it from an event handler: `await addLike(item.id)` in a `try/catch`. Commands cannot be called during render.

## Default invalidation

`form` invalidates all queries and load functions after success; `command` does nothing. Single-flight mutations let either refresh chosen queries in the same request.

## Server-driven

```js
export const createPost = form(schema, async (data) => {
	void getPosts().refresh();   // framework awaits it
	redirect(303, `/blog/${slug}`);
});
export const updatePost = form(v.object({ id: v.string() }), async (post) => {
	const result = externalApi.update(post);
	getPost(post.id).set(result);
});
```

Queries are keyed by argument, so the server finds the matching client instance. Calling `refresh()`, `set()` or `reconnect()` anywhere in a `form` handler replaces the default invalidation of all queries and load functions for that submission. For `query.live`, `getNotifications(userId).reconnect()` reconnects active clients in the same flight.

## Client-requested

When the server cannot know which instances are rendered, the client asks:

```js
await submit().updates(
	getPosts,                                  // all active instances
	getPosts({ filter: 'author:santa' }),      // one instance
	getPosts({ filter: 'author:santa' }).withOverride((posts) => [newPost, ...posts])
);
```

(`myCommand().updates(...)` for commands.) The server must accept via `requested` from `$app/server`:

```js
for (const { arg, query, ignore } of requested(getPosts, 10)) {
	if (arg.filter === 'author:santa') void query.refresh();
	else ignore();
}
await requested(getPosts, 1).refreshAll();   // shorthand
await requested(getPosts, 10).ignoreAll();
```

`arg` is the validated/transformed argument. Every requested update must be refreshed, set, reconnected or ignored, or that query errors on the client. The required `limit` guards against denial of service; requests beyond it fail on the client (`Infinity` is allowed but not recommended).

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block). One trim: the sentence that refresh(), set() or reconnect() anywhere in a handler replaces the default invalidation now says form handler, as the page does.
