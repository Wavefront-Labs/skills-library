---
id: computing-software.web-development.trpc.link-chain-and-terminating-link
name: link-chain-and-terminating-link
category: computing-software
field: web-development
product: trpc
tags: [trpc, links, terminating-link, client, splitlink]
level: practitioner
status: docs-checked
description: "Compose a tRPC client link chain that always ends in a terminating link, and pick between httpLink, httpBatchLink, stream, subscription, ws and local links."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Links customise the flow between client and server. The `links` array is a chain: links run in order on the request and in reverse on the response. Each link should do one thing, either modify an operation or cause a side effect such as logging.

```ts
export const trpc = createTRPCClient<AppRouter>({
  links: [loggerLink(), httpBatchLink({ url: 'http://localhost:3000' })],
});
```

The last link must be a terminating link, which sends the operation to the server instead of calling `next`. Without one, calls fail with `No more links to execute - did you forget to add an ending link?`. Anything listed after the terminating link never runs, so put `loggerLink`, `retryLink` and custom links before it.

Choosing the terminating link:
- `httpBatchLink`: recommended default; calls made in the same tick become one request.
- `httpLink`: one request per call; use to skip batching or send FormData and binary inputs.
- `httpBatchStreamLink`: batching with streamed responses; needed for async generators and nested promises in output.
- `httpSubscriptionLink`: subscriptions over Server-sent Events.
- `wsLink`: any operation over a WebSocket.
- `localLink`: call a router in the same process.

HTTP links do not handle subscriptions (they throw). Route by operation type with `splitLink`:

```ts
splitLink({
  condition: (op) => op.type === 'subscription',
  true: httpSubscriptionLink({ url: 'http://localhost:3000' }),
  false: httpBatchLink({ url: 'http://localhost:3000' }),
})
```

Each `splitLink` branch is its own chain and needs its own terminating link. If the server uses a data transformer, every terminating link in every branch needs the same `transformer`.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/links.md (Links Overview, The terminating link, Common mistakes). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
