---
id: computing-software.web-development.appwrite.appwrite-realtime-subscriptions
name: appwrite-realtime-subscriptions
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, realtime, subscriptions, channels, queries]
level: advanced
status: docs-checked
description: "Subscribe to live events from clients using Channel helpers, update or cancel subscriptions and filter with queries."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/realtime/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/realtime/subscribe/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/realtime/channels/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/realtime/queries/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/realtime/authentication/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stream changes into a client app.

Subscribe: `const sub = await realtime.subscribe(Channel.account(), (response) => { ... })`. Channels are built with the `Channel` helper, for example `Channel.tablesdb('<DB_ID>').table('<TABLE_ID>').row()`, `Channel.files()`, `Channel.bucket('<BUCKET_ID>').file()`, `Channel.teams()`, `Channel.memberships()`, `Channel.executions()`, `Channel.function('<FUNCTION_ID>')` and `Channel.presences()`.

Control: `subscription.update(...)` changes what is subscribed; `subscription.unsubscribe()` stops; `realtime.disconnect()` closes the connection. Realtime is for client SDKs; server SDKs are not supported.

Queries: pass queries as the third argument to `subscribe` to filter events server-side with `Query.equal` and friends, combined with `and`/`or`, and `isNull`, so the client receives only matching events.

Permissions: you only receive events for resources you may read; for public data use `Role.any()` read.

Authentication: a subscription made before authenticating keeps its old identity. On login or logout call `realtime.disconnect()` and subscribe again.

Gotcha: forgetting to disconnect and re-subscribe after a session change keeps the old identity.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): apis/realtime, apis/realtime/subscribe, apis/realtime/channels, apis/realtime/queries, apis/realtime/authentication. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Channel.functions() corrected to Channel.function(<FUNCTION_ID>); removed the invented Verify and the "many messages" note; queries are the third argument to subscribe; authentication wording changed to the page (disconnect then subscribe again).

Method: documentation only; no commands were run.
