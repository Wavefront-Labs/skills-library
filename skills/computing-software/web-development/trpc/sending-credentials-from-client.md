---
id: computing-software.web-development.trpc.sending-credentials-from-client
name: sending-credentials-from-client
category: computing-software
field: web-development
product: trpc
tags: [trpc, authentication, cookies, headers, connectionparams]
level: practitioner
status: docs-checked
description: "How credentials reach createContext: cookies for same-origin, headers option on HTTP links, SSE limits, and WebSocket connection params."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/authorization.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpSubscriptionLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The authorization docs list how a client can send credentials:

- Cookies are sent with every request when client and server share an origin. For another origin see the CORS and cookies page.
- Headers such as `Authorization` can be set on any HTTP link using the `headers` option.
- Subscriptions over SSE cannot send custom headers with the browser's `EventSource`; see the `httpSubscriptionLink` options (cookies, or headers via an EventSource ponyfill).
- WebSockets send connection params when the connection opens, which `createContext` reads from `opts.info.connectionParams`.

Common mistakes listed in the docs:

1. Calling `opts.next()` without the narrowed `ctx`: later procedures still see `ctx.user` as nullable. Pass `opts.next({ ctx: { user: opts.ctx.user } })`.
2. Throwing in `createContext` for a missing or invalid token. That fails every procedure in the request, public ones too. Return `user: null` and let a middleware reject the procedures that need a user.
3. Putting tokens in `httpSubscriptionLink`'s `connectionParams`. They are sent in the URL where servers and proxies may log them. Prefer cookies, or headers through an EventSource ponyfill.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/authorization.md (read in full): "Sending credentials from the client" bullets and "Common mistakes"; www/v11/docs/client/links/httpSubscriptionLink.md (read in full): cookies on the same domain, withCredentials cross-domain, ponyfilled headers and the connectionParams-in-URL note. The CORS and cookies page (client/cors.md) was not opened, so the skill only points to it.

Removed or corrected: the "configured on both sides" claim (not on the authorization page) and the invented Verify step.

Method: documentation only; no commands were run.
