---
id: computing-software.software-engineering.api-design.graphql-schema-design
name: graphql-schema-design
category: computing-software
field: software-engineering
product: api-design
tags: [graphql, api-design, schema-design, dataloader, n-plus-one, query-complexity, apollo, relay, breaking-changes, deprecation, persisted-queries]
level: advanced
status: draft
description: "Design a GraphQL schema that avoids resolver N+1 queries (DataLoader), query-cost abuse, and breaking changes via additive evolution."
sources: ["GraphQL spec and graphql.org best practices", "Relay Cursor Connections spec", "Apollo docs - DataLoader pattern, schema design"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GraphQL schema design — the resolver N+1 problem and query-cost abuse

**Goal:** a schema whose resolvers don't silently issue hundreds of DB queries per
request, and that a client can't accidentally (or deliberately) turn into a DoS.

## 1. The N+1 problem is the default behavior, not an edge case
```graphql
type Post { id: ID!, author: User! }
```
A naive resolver for `author` runs one query per `Post` in the list — 100 posts, 100
queries. **DataLoader** (or an equivalent batching layer) fixes this by collecting
all the keys requested during one tick of the event loop and issuing a single
batched query:
```js
const userLoader = new DataLoader(ids => db.users.findByIds(ids));
// resolver: return userLoader.load(post.authorId);
```
This is not optional polish — any GraphQL schema with relational fields needs a
batching layer from day one, or performance degrades silently in proportion to list
size, invisible in a test with 3 items and severe in production with 300.

## 2. Query cost / complexity limits
A client (malicious or just a badly-written frontend) can request deeply nested
fields (`friends { friends { friends { posts { comments { author { friends ...}}}}}}`)
that fans out exponentially — rate limiting by request count doesn't catch this,
since it's one request. Mitigate with:
- **Depth limiting** — reject queries beyond a fixed nesting depth.
- **Cost analysis** — assign a weight per field/connection and reject queries over a
  budget (graphql-cost-analysis, Apollo's cost directives).
- **Pagination required on every list field** — never expose an unbounded list field
  (`allUsers: [User!]!`); use connections (`allUsers(first: Int!): UserConnection!`)
  so a client can't accidentally request everything.

## 3. Evolve additively; deprecate, don't remove
```graphql
type User {
  name: String! @deprecated(reason: "use displayName")
  displayName: String!
}
```
Adding a field or type is always backward-compatible — clients that don't query it
are unaffected. Removing or renaming a field, or changing a field's type/nullability,
breaks any client still querying it with no compile-time warning on the server side
(unlike a typed REST client). Use `@deprecated` and give clients a real migration
window (tracked via query analytics on who's still requesting the deprecated field)
before actually removing it. Changing nullable→non-nullable is also breaking: it can
crash existing clients expecting `null` to be possible.

## 4. Connections (cursor pagination) over offset for any list that mutates
```graphql
type PostConnection { edges: [PostEdge!]!, pageInfo: PageInfo! }
type PostEdge { node: Post!, cursor: String! }
```
Offset-based pagination (`skip`/`limit`) shifts under concurrent inserts/deletes —
page 2 can repeat or skip items. Cursor-based pagination (Relay's connection spec) is
stable under mutation because the cursor encodes a position relative to a specific
item, not an index.

## 5. Error handling: partial success is normal, design for it
A GraphQL response can have `data` with some fields populated and `errors` listing
which specific field failed — unlike REST's all-or-nothing status code. Nullable
fields that can legitimately fail (an external service call inside one resolver)
should be nullable in the schema so one failing field doesn't null out the entire
response; a non-nullable field whose resolver can throw propagates the null up to the
nearest nullable ancestor, which can wipe out much more of the response than intended
("null bubbling") — think carefully about nullability as a contract, not just a type
annotation.

## Gotchas
- Mutations should return the full updated object (or at least the fields the client
  is likely to need next), not just a boolean — avoids a forced extra round-trip.
- Persisted queries (client sends a hash, server has the full query registered) close
  off a major DoS vector (arbitrary ad-hoc queries) at the cost of needing a build step
  to register queries — worth it for a public-facing API, often unnecessary for
  internal-only.
- Introspection should be disabled in production for a public API that doesn't want
  its full schema (and thus its data model) visible to anyone.

## Verify
- [ ] Every relational/list field resolver uses a batching loader, confirmed by
      logging query count for a request with N items in a list (should stay
      constant as N grows, not scale linearly).
- [ ] Every list field is a connection with a required `first`/`last` argument, no
      unbounded list field exists.
- [ ] A query-cost or depth limit is enforced and tested with a deliberately
      deep/wide query.
- [ ] No field has been removed without a deprecation window; query analytics
      confirm zero traffic before actual removal.

Related: computing-software.software-engineering.api-design.rest-resource-design-and-versioning
