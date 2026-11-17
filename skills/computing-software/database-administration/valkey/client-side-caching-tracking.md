---
id: computing-software.database-administration.valkey.client-side-caching-tracking
name: client-side-caching-tracking
category: computing-software
field: database-administration
product: valkey
tags: [client-side-caching, tracking, invalidation, bcast, optin, noloop, resp3]
level: practitioner
status: docs-checked
description: "Valkey client-side caching via CLIENT TRACKING: default and BCAST modes, REDIRECT, OPTIN, NOLOOP, invalidation messages, RESP2 vs RESP3, race condition."
sources:
  - https://valkey.io/topics/client-side-caching/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Client-side caching keeps hot replies in application memory, cutting latency and server load. The hard part is invalidation; Valkey supports it natively as Tracking, off by default per connection (`CLIENT TRACKING ON`).

Default mode: the server records which keys a client read and sends an invalidation message when one is modified, expired, or evicted by maxmemory. Memory is bounded by a global Invalidation Table of client IDs (not pointers); when full, an old entry may be evicted by sending a fake invalidation. There is one keyspace across all databases, so a change in another database still invalidates. A flush sends a null message.

Delivery: with RESP3 (`HELLO`), invalidations arrive as push messages on the same connection. With RESP2 use two connections: get the invalidation connection ID with `CLIENT ID`, subscribe it to `__redis__:invalidate`, then on the data connection run `CLIENT TRACKING on REDIRECT <id>`. Only the redirect target receives the message.

Opt-in: `CLIENT TRACKING on REDIRECT 1234 OPTIN`, then send `CLIENT CACHING YES` immediately before the read you want tracked (a following MULTI or Lua script tracks all its commands).

Broadcasting: `CLIENT TRACKING on REDIRECT 10 BCAST PREFIX object: PREFIX user:` uses no server memory, notifies on any key under the prefix, and no prefix means every key. Prefixes may not overlap (`foo` and `foob`). CPU grows with prefix count.

`NOLOOP` stops notifications for your own writes. Race: an invalidation can arrive before the slow GET reply, so store a placeholder such as caching-in-progress first and drop it if invalidated.

## Checked
2026-11-03. Confirmed against the Valkey Client-side caching page (valkey.io/topics/client-side-caching/): default and BCAST modes, the Invalidation Table with client IDs and fake invalidations, single keyspace across databases, null message on flush, RESP2 two-connection setup with `__redis__:invalidate`, RESP3 push messages, OPTIN with `CLIENT CACHING YES` (MULTI and Lua tracked), BCAST prefix rules and CPU cost, NOLOOP, and the placeholder race fix. Nothing removed.
Method: documentation only; no commands were run.
