---
id: computing-software.web-development.directus.realtime-auth-modes-graphql
name: realtime-auth-modes-graphql
category: computing-software
field: web-development
product: directus
tags: [realtime-auth-modes, handshake-mode, strict-mode, graphql-subscriptions]
level: advanced
status: docs-checked
description: "Choose Directus Realtime auth modes (public, handshake, strict), send auth messages, and use GraphQL subscriptions through graphql-ws."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/07.realtime/1.authentication.md
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/07.realtime/2.subscriptions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Modes (one per project): `public` (no auth, public role only), `handshake` (default; connect freely, the first message must authenticate before the timeout), `strict` (token required on connect). Self-hosted: set `WEBSOCKETS_REST_AUTH`, `WEBSOCKETS_GRAPHQL_AUTH`, `WEBSOCKETS_LOGS_AUTH`.

Handshake first message, any one of:

```json
{ "type": "auth", "access_token": "..." }
{ "type": "auth", "email": "user@email.com", "password": "..." }
{ "type": "auth", "refresh_token": "..." }
```

Success returns `{ "type": "auth", "status": "ok" }`, with a `refresh_token` when you used email/password or refresh. On an auth-expired error send a new auth message within the timeout or the connection closes.

Strict: add `?access_token=...` to the connection URL. An expired token closes the connection with `Forbidden`; refresh and reconnect.

GraphQL (graphql-ws): only `access_token` is supported.

```js
const client = createClient({ url: "ws://your-directus-url/graphql", keepAlive: 30000,
  connectionParams: async () => ({ access_token: "MY_TOKEN" }) });
```

Subscribe with `subscription { posts_mutated(event: create) { key data { text } } }`; stop with `client.dispose()`. Deletes fill only `key`.

## Checked

2026-11-04: confirmed against the Directus docs Authentication and Subscriptions pages: three modes and handshake default, environment variables, auth message forms and confirmation, expired-auth timeout, strict URL parameter and Forbidden close, GraphQL access_token only, posts_mutated subscription, dispose.

Method: documentation only; no commands were run.
