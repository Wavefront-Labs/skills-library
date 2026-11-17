---
id: computing-software.web-development.trpc.subscriptions-async-generators
name: subscriptions-async-generators
category: computing-software
field: web-development
product: trpc
tags: [trpc, subscription, async-generator, sse, websockets]
level: practitioner
status: docs-checked
description: "Define a subscription as an async generator that yields events, wired to an EventEmitter with opts.signal; choose SSE or WebSockets transport."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/subscriptions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Subscriptions are real-time event streams: the client holds a persistent connection and tRPC reconnects and recovers when it drops (with `tracked()` ids). A subscription is an async generator function (the page says observable subscriptions are deprecated).

```ts
import EventEmitter, { on } from 'node:events';

const ee = new EventEmitter();

export const appRouter = t.router({
  onPostAdd: t.procedure.subscription(async function* (opts) {
    // listen for new events
    for await (const [data] of on(ee, 'add', {
      // the request AbortSignal cancels the emitter listener when the request is aborted
      signal: opts.signal,
    })) {
      yield data as Post;
    }
  }),
});
```

Transport choice: WebSockets (see the websockets pages) or Server-sent Events through `httpSubscriptionLink`. If unsure the docs recommend SSE: it is easier to set up and needs no WebSocket server.

Pass `opts.signal` to what you are waiting on (like `on(ee, 'add', { signal })` above), or check `opts.signal.aborted` in loops; otherwise the generator can keep waiting, with its listeners attached, after the client is gone. The reference projects are a minimal Node.js WebSocket example (`examples/standalone-server`), a full-stack SSE chat on TanStack Start, and a Next.js + Prisma WebSockets starter.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/subscriptions.md (read in full, including the output validation helper and Common mistakes): introduction, WebSockets or SSE recommendation, reference projects table, basic example, and the opts.signal guidance.

Removed or corrected: the claims that signal should be passed to timers and fetches (the page names event emitters and loops), and the invented Verify step about listener counts.

Method: documentation only; no commands were run.
