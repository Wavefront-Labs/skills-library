---
id: computing-software.web-development.trpc.subscriptions-output-validation
name: subscriptions-output-validation
category: computing-software
field: web-development
product: trpc
tags: [trpc, subscription, output-validation, zod, async-iterable]
level: sme
status: docs-checked
description: "Validate subscription output with a zod schema helper that wraps the async iterable, optionally keeping tracked envelopes intact."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/subscriptions.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Because subscriptions are async iterators, output validation must go through the iterator. The docs provide a Zod v4 helper, `zAsyncIterable`, that:

1. checks the value is an async iterable,
2. validates every yielded item against `yield`,
3. optionally validates the generator return value (`return`, not applicable to subscriptions),
4. supports `tracked: true` so tracked envelopes keep their id while the data is validated.

Its core is a `z.custom<AsyncIterable<...>>(isAsyncIterable).transform(async function* (iter) { ... })` that loops with `iterator.next()`, parses each value with `opts.yield.parseAsync(...)` (for tracked ones it first reads `[id, data]` from the envelope using `isTrackedEnvelope` and re-yields `tracked(id, parsedData)`), and calls `iterator.return?.()` in `finally`.

Then use it in `.output()`:

```ts
onPostAdd: publicProcedure
  .output(zAsyncIterable({ yield: postSchema, tracked: true }))
  .subscription(async function* (opts) {
    yield tracked(post.id, post);
  })
```

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/subscriptions.md (read in full): "Output validation" with the full `zAsyncIterable` helper (Zod v4) and its use in `.output()`; www/v11/docs/server/validators.md (read in full): the pointer that subscriptions can use the same validation techniques.

Removed or corrected: the unsourced rationale paragraph (leaking fields, why `finally` matters) and the invented Verify step.

Method: documentation only; no commands were run.
