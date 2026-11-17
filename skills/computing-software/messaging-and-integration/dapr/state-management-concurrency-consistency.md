---
id: computing-software.messaging-and-integration.dapr.state-management-concurrency-consistency
name: state-management-concurrency-consistency
category: computing-software
field: messaging-and-integration
product: dapr
tags: [state, etag, occ, consistency, transactions, bulk, actor-state, query, ttl, state-store]
level: practitioner
status: docs-checked
description: "Dapr state API: last-write-wins default, ETag optimistic concurrency, strong versus eventual consistency, bulk and transactions, actorStateStore, and direct store queries."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/state-management/state-management-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The state API saves, reads and queries key/value pairs in a pluggable state store component: HTTP POST to save or query, GET to read a key.

Defaults: assume the store is eventually consistent and uses last-write-wins.

Concurrency uses ETags (optimistic concurrency control). Dapr attaches an ETag to every returned value. Updates send the ETag in the request body; deletes send it in the `If-Match` header. The write succeeds only if it matches the stored ETag, giving first-write-wins. If you omit ETags, Dapr skips the check. Stores without native ETags have them simulated by their Dapr implementation.

Consistency: eventual (default) returns once the store accepts the write, even on one replica; strong waits for all replicas or designated quorums to acknowledge.

Content type is optional metadata the component may use: HTTP query parameter `metadata.contentType` (for example `http://localhost:3500/v1.0/state/store?metadata.contentType=application/json`), or `"contentType"` in gRPC metadata.

Multiple operations: bulk read sends individual reads to the store and returns one result; transactional writes group write, update and delete as one atomic request.

Actor state: set `actorStateStore` to `true` in the component metadata (needs a transactional store; only one state store component can serve all actors), and always set `ttlInSeconds` so state eventually disappears.

Querying: use the optional query API, or query the store natively. Direct queries bypass Dapr concurrency control, so treat them as read-only snapshots. Redis example: `KEYS "myApp*"`. Actor keys look like `<app-id>||<actor-type>||<actor-id>||<key>`.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; wording tightened where it went beyond the page, the remaining claims are unchanged.

Method: documentation only; no commands were run.
