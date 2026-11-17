---
id: computing-software.web-development.trpc.sse-ping-timeout-configuration
name: sse-ping-timeout-configuration
category: computing-software
field: web-development
product: trpc
tags: [trpc, sse, ping, reconnectafterinactivityms, subscriptions]
level: advanced
status: docs-checked
description: "Keep SSE subscriptions alive with server ping, reconnectAfterInactivityMs, maxDurationMs and emitAndEndImmediately set in initTRPC.create sse options."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpSubscriptionLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSE behaviour is configured on the server through `initTRPC.create({ sse: { ... } })`. The `client` options are sent to the client as part of the first message.

```ts
export const t = initTRPC.create({
  sse: {
    // maxDurationMs: 60_000,
    ping: { enabled: true, intervalMs: 2_000 },
    client: { reconnectAfterInactivityMs: 3_000 },
  },
});
```

Options:
- `ping.enabled` (default false) and `ping.intervalMs` (default 1000): the server sends ping comments to keep the connection alive.
- `client.reconnectAfterInactivityMs`: if no message, including pings, arrives within this time, the connection is marked "connecting" and reconnects.
- `maxDurationMs` (default undefined): maximum duration in milliseconds for the request before ending the stream.
- `emitAndEndImmediately` (default false): end the request right after data is sent; only for serverless runtimes that cannot stream responses.

The page says ping is particularly useful combined with `reconnectAfterInactivityMs`; its examples use a 2 second ping interval and a 3 second inactivity timeout.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/client/links/httpSubscriptionLink.md (read in full): "Timeout Configuration", "Server Ping Configuration" and the `SSEStreamProducerOptions` block with defaults.

Removed or corrected: the claims that the client reconnects when maxDurationMs ends the stream, that proxies see ping activity, the advice that the timeout must exceed the ping interval, the tracked() pairing (not on this page), and the invented Verify step.

Method: documentation only; no commands were run.
