---
id: computing-software.web-development.trpc.subscriptions-stop-and-cleanup
name: subscriptions-stop-and-cleanup
category: computing-software
field: web-development
product: trpc
tags: [trpc, subscription, cleanup, try-finally, generator-return]
level: practitioner
status: docs-checked
description: "Stop a subscription from the server by returning from the generator and release resources with try...finally, which tRPC triggers via generator.return()."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/subscriptions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Stopping from the server: simply `return` in the generator function. The client is disconnected.

```ts
.subscription(async function* (opts) {
  let index = opts.input.lastEventId ?? 0;
  while (!opts.signal!.aborted) {
    const idx = index++;
    if (idx > 100) {
      // the subscription stops and the client disconnects
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
}),
```

On the client you `.unsubscribe()`.

Cleaning up side effects: tRPC calls `.return()` on the generator instance whenever the subscription stops for any reason, so use `try...finally`:

```ts
.subscription(async function* (opts) {
  let timeout: ReturnType<typeof setTimeout> | undefined;
  try {
    for await (const [data] of on(ee, 'add', { signal: opts.signal })) {
      timeout = setTimeout(() => console.log('doing work'));
      yield data as Post;
    }
  } finally {
    if (timeout) clearTimeout(timeout);
  }
}),
```

Error behaviour: throwing in the generator reaches `onError()` on the backend; a 5xx error makes the client reconnect from the last tracked id, other errors cancel the subscription and propagate to the client `onError` callback.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/subscriptions.md (read in full): "Stopping a subscription from the server", "Cleanup of side effects" and "Error handling".

Removed or corrected: the list of things to clean up (timers, DB listeners, locks, brokers; not on the page) and the invented Verify step.

Method: documentation only; no commands were run.
