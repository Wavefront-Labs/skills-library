---
id: computing-software.web-development.trpc.subscriptions-tracked-resume
name: subscriptions-tracked-resume
category: computing-software
field: web-development
product: trpc
tags: [trpc, subscription, tracked, lasteventid, reconnect]
level: advanced
status: docs-checked
description: "Yield tracked(id, data) so clients reconnect with the last event id and resume without missing events; subscribe to the source before backfilling."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/subscriptions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If you `yield tracked(id, data)`, the client automatically reconnects after a disconnect and sends the last known id. You can pass an initial `lastEventId` when starting the subscription, and it is updated as data arrives.

- SSE: this is part of the EventSource spec and arrives as `lastEventId` in your `.input()`.
- WebSockets: `wsLink` sends the last known id and updates it itself.

```ts
onPostAdd: publicProcedure
  .input(z.object({ lastEventId: z.string().nullish() }).optional())
  .subscription(async function* (opts) {
    // subscribe first so we do not miss events while fetching the backlog
    const iterable = ee.toIterable('add', { signal: opts.signal });

    if (opts.input?.lastEventId) {
      // get posts since the last event id and yield them
      // for (const item of items) yield tracked(item.id, item);
    }
    for await (const [data] of iterable) {
      const post = data as Post;
      yield tracked(post.id, post);
    }
  }),
```

Ordering rule from the docs: if capturing every event is critical, set up the event listener before querying the database for events after `lastEventId`, otherwise events emitted during the backfill are lost.

Client side, `onData` receives `{ id, data }` for tracked events.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/subscriptions.md (read in full): the `tracked()` section with its SSE and WebSockets bullets, the tip about listening before fetching, the example, and the client `{ id, data }` shape. Every claim matched the page text.

Removed or corrected: the invented Verify step; no other claim needed changing.

Method: documentation only; no commands were run.
