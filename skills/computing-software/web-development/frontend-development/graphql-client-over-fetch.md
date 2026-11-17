---
id: computing-software.web-development.frontend-development.graphql-client-over-fetch
name: graphql-client-over-fetch
category: computing-software
field: web-development
product: frontend-development
tags: [graphql-client, graphql, persisted-queries, graphql-codegen, apollo-client, urql]
level: practitioner
status: docs-checked
description: "Calling GraphQL APIs from the browser: request shape, 200-with-errors handling, variables not interpolation, persisted queries, codegen typing and client cache choices."
sources:
  - https://graphql.org/learn/serving-over-http/
  - https://www.apollographql.com/docs/apollo-server/performance/apq
  - https://the-guild.dev/graphql/codegen/docs/guides/react-vue
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL client over fetch

## 1. Minimal client
```ts
async function gql<T>(query: string, variables?: Record<string, unknown>, signal?: AbortSignal): Promise<T> {
  const res = await fetch("/graphql", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/graphql-response+json, application/json" },
    body: JSON.stringify({ query, variables }),
    signal,
  });
  const body = await res.json();
  if (!res.ok && !body.errors) throw new Error(`HTTP ${res.status}`);
  if (body.errors?.length) throw Object.assign(new Error(body.errors[0].message), { errors: body.errors, data: body.data });
  return body.data;
}
```
- Classic servers return **HTTP 200 with an `errors` array**; `data` may be partially filled. Decide per screen whether partial data renders.
- Branch on a stable error code your server documents (often under `extensions`), not on message text.

## 2. Variables, never string building
```graphql
query Product($id: ID!) { product(id: $id) { id name price { amount currency } } }
```
Interpolating values into the query string breaks caching (every query unique) and invites injection.

## 3. Persisted queries
APQ (Apollo Server's automatic persisted queries): the client first sends a hash of the query, and resends the full query if the server does not know it; see the Apollo APQ page for the exact request shape. Allowlisting known queries at build time also blocks arbitrary queries in production.

## 4. Typing
GraphQL Code Generator generates TypeScript types from your schema and documents (see the React/Vue guide); regenerate in dev and check in CI that documents still validate.

## 5. Client choice
| Need | Use |
|---|---|
| Few queries, server components | plain fetch / `graphql-request` |
| Normalised cache, optimistic updates | Apollo Client, urql + Graphcache, Relay |
| Already on TanStack Query | `useQuery({ queryKey: ["product", id], queryFn: () => gql(...) })` |
Normalised caches key by `__typename` + `id`: always select `id` on entities.

## Gotchas
- Over-fetching moves to the server: deep queries can be expensive; servers should enforce depth/complexity limits.
- File uploads are not in the spec (multipart extension); prefer presigned URLs.

## Verify
- [ ] Error-path test: server returns `{ data: null, errors: [...] }` with 200 and the UI shows the error.

## Checked
2026-10-28. Confirmed on graphql.org serving-over-http: `application/graphql-response+json` in Accept (with `application/json` for legacy servers), HTTP 2xx for responses with non-null `data` even with errors. Apollo APQ page: hash-then-resend flow. Removed: error code names, exact APQ field names and GET-cacheability claim, codegen preset and flag names (not confirmed).
Method: documentation only; no commands were run.
