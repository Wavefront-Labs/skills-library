---
id: computing-software.software-engineering.api-design.graphql-relay-connections
name: graphql-relay-connections
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, relay-connections, cursor-pagination, pageinfo, edges]
level: practitioner
status: docs-checked
description: "Implement Relay cursor connections in GraphQL: edges, nodes, pageInfo, first/after and last/before, opaque cursors and bounded page sizes."
sources: ["https://relay.dev/graphql/connections.htm", "https://graphql.org/learn/pagination/", "https://www.apollographql.com/docs/react/pagination/cursor-based"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relay connections and cursor pagination

## Schema (Relay Cursor Connections spec)
```graphql
type Query { orders(first: Int, after: String, last: Int, before: String, filter: OrderFilter): OrderConnection! }
type OrderConnection { edges: [OrderEdge!]!, nodes: [Order!]!, pageInfo: PageInfo!, totalCount: Int }
type OrderEdge { cursor: String!, node: Order! }
type PageInfo { hasNextPage: Boolean!, hasPreviousPage: Boolean!, startCursor: String, endCursor: String }
```
The Relay spec requires `edges` and `pageInfo` on a type whose name ends in `Connection`, and `node` and
`cursor` on an edge type (`node` cannot be a list). `nodes` is an optional shortcut that graphql.org describes
as a dedicated list of just the nodes; edges exist to carry per-relationship data and the cursor.
`PageInfo` must have non-null `hasPreviousPage` and `hasNextPage`, plus `startCursor` and `endCursor`
(null when there are no results).

## Server rules
- Cursors are **opaque**: for example base64 of the keyset values (`{"created_at":"...","id":"o9"}`),
  maybe signed. graphql.org suggests base64 to signal that the format must not be relied on. Clients must
  not construct them.
- Back them with keyset queries: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT first+1`;
  fetching one extra row tells you `hasNextPage` without a count.
- Enforce a maximum: require `first` or `last`, cap it at a documented limit, error otherwise
  (design guidance; the spec leaves limits to you). Avoid supporting `first` and `last` together:
  the spec strongly discourages it, and a negative value must be an error.
- Edge order must be the same for `first/after` and `last/before`; `hasNextPage` must be accurate for
  `first/after`, while `hasPreviousPage` only must be accurate for `last/before` (the other direction may
  be false when it cannot be determined efficiently).
- `totalCount` is expensive; resolve it only when selected and consider an estimate.
- Same cursor must remain valid if rows are inserted elsewhere; keyset cursors do, offsets don't.
- Nested connections (`users { orders(first: 50) }`) multiply cost: include them in query cost
  analysis and batch with DataLoader keyed by parent id.

## Client
Apollo Client's `relayStylePagination()` field policy merges pages; fetch more with `fetchMore`
passing the previous page's `pageInfo.endCursor` as the cursor variable.

## Checked
2026-11-08. Confirmed by reading the Relay Cursor Connections spec in full, plus graphql.org pagination
(opaque cursors, base64 suggestion, `nodes` list, `startCursor`/`endCursor`) and the Apollo cursor-based
pagination page (`relayStylePagination`, `fetchMore`, `endCursor`; read by targeted search).
Removed: GitHub attribution for `nodes`, the "cap at 100 (GitHub's rule)" claim and `usePaginationFragment`
(none in the cited pages). Keyset SQL, DataLoader, cost-analysis and `totalCount` advice are design
guidance, not from the sources.
Method: documentation only; no commands were run.
