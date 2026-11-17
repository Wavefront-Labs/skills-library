---
id: computing-software.web-development.sveltekit.sveltekit-remote-query-batch-live
name: sveltekit-remote-query-batch-live
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, remote-functions, remote-query-batch-live, query-batch, query-live, streaming]
level: advanced
status: docs-checked
description: "Use query.batch to solve n+1 lookups and query.live for streaming real-time data, including connected, reconnect() and for-await use."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/20-core-concepts/60-remote-functions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick the right query variant for batching or real-time data.

## query.batch

Batches calls that happen in the same macrotask, avoiding n+1 database calls. The server callback gets an array of arguments and must return `(input, index) => output`:

```js
export const getWeather = query.batch(v.string(), async (cityIds) => {
	const weather = await db.sql`
		SELECT * FROM weather WHERE city_id = ANY(${cityIds})
	`;
	const lookup = new Map(weather.map(w => [w.city_id, w]));
	return (cityId) => lookup.get(cityId);
});
```

Components then simply call `await getWeather(city.id)` inside an `{#each}`; the calls group together.

## query.live

For real-time data: the callback, typically an async generator, returns an `AsyncIterable`.

```js
export const getTime = query.live(async function* () {
	while (true) {
		yield new Date();
		await new Promise((f) => setTimeout(f, 1000));
	}
});
```

- During SSR, `await getTime()` returns the first yielded value then closes the iterator; that value is reused in hydration.
- On the client the query stays connected while used; multiple instances share a connection; with no active uses it disconnects and server iteration stops.
- Instances expose `connected` and `reconnect()`: `<p>connected: {time.connected}</p>` and `time.reconnect()`.
- If the connection drops, `connected` becomes `false`; SvelteKit reconnects passively with exponential backoff and actively when `navigator.onLine` goes false to true.
- No `refresh()` method, since live queries are self-updating.

## Imperative use

Live query instances are async-iterable: `for await (const value of getTime()) { ... }`. The first value is the most recently received one if available; if values arrive faster than consumed only the latest pending is kept (not an event log). All consumers share one connection; on the server a `for await` joins a per-request shared iteration.

## Gotcha

Never cache live query responses in a service worker: the cloned response keeps streaming after the page closes. Exclude responses whose `Cache-Control` includes `no-store`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 60-remote-functions.md (all 1353 lines, every code block), query.batch and query.live sections. No claims trimmed.
