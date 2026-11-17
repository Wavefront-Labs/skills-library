---
id: computing-software.web-development.trpc.http-subscription-link-setup-and-auth
name: http-subscription-link-setup-and-auth
category: computing-software
field: web-development
product: trpc
tags: [trpc, httpsubscriptionlink, sse, eventsource, authentication]
level: practitioner
status: docs-checked
description: "Set up httpSubscriptionLink behind a splitLink and authenticate EventSource with cookies, withCredentials, a ponyfill with headers, or connectionParams."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpSubscriptionLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`httpSubscriptionLink` is a terminating link that uses Server-sent Events for subscriptions, which is easier than running a WebSocket server. Use a `splitLink` so subscriptions go to it and everything else to a batch link (see `computing-software.web-development.trpc.link-chain-and-terminating-link`).

Authentication options:
- Same domain web apps: cookies are sent automatically.
- Cross-domain web apps: `eventSourceOptions() { return { withCredentials: true }; }`.
- Non-web or custom headers: ponyfill `EventSource` with `event-source-polyfill` and populate headers in the callback, which receives `{ op }` and may be async:

```ts
httpSubscriptionLink({
  url: 'http://localhost:3000',
  EventSource: EventSourcePolyfill,
  eventSourceOptions: async ({ op }) => ({
    headers: { authorization: 'Bearer supersecret' },
  }),
})
```

- `connectionParams`: object or async function; serialized into the URL (which is why the docs prefer the other methods) and read on the server as `opts.info.connectionParams?.token` inside `createContext`.

Renewing expired auth: native `EventSource` retries automatically but will not re-run `url()` or `eventSourceOptions()`. Put a `retryLink` before `httpSubscriptionLink` in the `true` branch, retrying on `UNAUTHORIZED` or `FORBIDDEN`, so the link is recreated with fresh config. Restarting recreates the EventSource, so previously tracked events are lost.

If the environment lacks `EventSource`, install a polyfill. React Native needs ponyfills for EventSource, Streams and async iterators (rn-eventsource-reborn, web-streams-polyfill, @azure/core-asynciterator-polyfill); avoid XMLHttpRequest-based EventSource polyfills, which fail to reconnect after backgrounding.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/links/httpSubscriptionLink.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the 'most to least preferred' ordering the page does not state.

Method: documentation only; no commands were run.
