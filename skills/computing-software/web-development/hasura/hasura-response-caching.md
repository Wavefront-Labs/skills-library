---
id: computing-software.web-development.hasura.hasura-response-caching
name: hasura-response-caching
category: computing-software
field: web-development
product: hasura
tags: [hasura, caching, cached-directive, performance, enterprise]
level: advanced
status: docs-checked
description: "Cache Hasura query responses with the @cached directive, ttl and refresh arguments, cache-key headers, and clear entries via the cache clear endpoint."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/caching/caching-config.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/caching/how-it-works.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/caching/enterprise-caching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speed up repeated read queries (Hasura Cloud and Enterprise Edition).

Add the directive to a query:

```graphql
query MyCachedQuery @cached(ttl: 120) {
  users { id name }
}
```
Rules from the docs:
- Entries live in an LRU cache with a TTL that defaults to 60 seconds; the maximum allowed `ttl` is 300 seconds on Hasura Cloud.
- `@cached(refresh: true)` forces a refresh; the value must be a literal boolean, not a variable (a variable causes a cache miss because it is treated as a different query).
- Response headers: `Cache-Control: max-age={SECONDS}`, `X-Hasura-Query-Cache-Key` and `X-Hasura-Query-Family-Cache-Key` (family ignores variable values).
- The cache key is a hash of the query text, operation name, variables, the role and the session variables needed by the query's permissions, and request headers for Remote Schemas or Actions with `forward_client_headers` true. Only whitespace differences are ignored in the query text.
- Writes to the cache are rate limited (leaky bucket); over the limit the response carries `Warning: 199 - cache-store-capacity-exceeded`.

Clear entries (POST):
- `/pro/cache/clear` clears all.
- `/pro/cache/clear?key={HASH}` clears one key.
- `/pro/cache/clear?family={FAMILY}` clears a query family.

Enterprise Edition needs a Redis instance co-located with the engine, set with `HASURA_GRAPHQL_REDIS_URL`. Tuning env vars: `HASURA_GRAPHQL_CACHE_MAX_ENTRY_TTL` (default 3600 seconds), `HASURA_GRAPHQL_CACHE_MAX_ENTRY_SIZE` (default 1000 MB), `HASURA_GRAPHQL_CACHE_BUCKET_RATE`, `HASURA_GRAPHQL_CACHE_BUCKET_SIZE`, `HASURA_GRAPHQL_CACHING_REDIS_POOL_SIZE` (default 500).

Gotcha: invalidation is TTL-based. Hasura has no automatic invalidation, for example on specific mutations; use the clear endpoints.

## Checked
2026-11-07. Read in full all three cited pages (caching-config.mdx, how-it-works.mdx, enterprise-caching.mdx; GitHub file view, no snippet files).
Confirmed: every item above, including the defaults and the clear endpoints.
Removed: "mutations are not cached" (not stated; only the lack of automatic invalidation is), the invented Verify step; corrected the example to use a named query as on the page.
Method: documentation only; no commands were run.
