---
id: computing-software.web-development.drizzle-orm.drizzle-query-caching
name: drizzle-query-caching
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, cache, upstash, withcache, invalidation]
level: advanced
status: docs-checked
description: "Opt in to query caching in Drizzle with upstashCache or a custom Cache, use $withCache per query, global mode, tags and invalidation."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add caching without hidden behavior.

Default: no caching at all (`explicit` strategy, i.e. `global: false`); you must opt in. Mutations still trigger the cache's `onMutate` handler, which tries to invalidate cached queries that involved the affected tables.

```ts
import { upstashCache } from "drizzle-orm/cache/upstash";
const db = drizzle(process.env.DB_URL!, {
  cache: upstashCache({ url: '<UPSTASH_URL>', token: '<UPSTASH_TOKEN>', global: false, config: { ex: 60 } }),
});
await db.select().from(users).$withCache();
```

`upstashCache()` uses Upstash Redis with automatic configuration if the environment variables are set; `url` and `token` are optional.

`$withCache` options per query: `{ config: {...} }` (rewrite the config for this query), `{ tag: 'custom_key' }` (custom cache key instead of hashing query and params), `{ autoInvalidate: false }`. `autoInvalidate` is enabled by default; turning it off gives eventual consistency: after an insert the cached query keeps returning old data until its TTL expires (the docs example uses `ex: 3`). The docs suggest it only for rarely changing data or manual invalidation and recommend keeping the default in most cases.

Global mode (`global: true`): every select looks in cache first; opt out per query with `.$withCache(false)`.

Invalidate manually through the instance:

```ts
await db.$cache.invalidate({ tables: [users, posts] });
await db.$cache.invalidate({ tables: ["usersTable"] });
await db.$cache.invalidate({ tags: ["custom_key"] });
```

`tables` and `tags` each accept a single value or an array; tables may be given by table object or by name.

Config: `ex` is expiration in seconds. The custom-cache `CacheConfig` type also lists `px` (ms), `exat`, `pxat`, `keepTtl` and `hexOptions`; the Upstash reference lists only `ex` and `hexOptions`.

Custom cache: extend `Cache` and implement `strategy()` (`'explicit' | 'all'`), `get(key)`, `put(key, response, tables, isTag, config)` and `onMutate({ tags, tables })`; the docs example uses Keyv and tracks which keys each table was used in, for invalidation.

Limitations per the docs: not handled for raw queries (`db.execute(sql...)`) or inside transactions. Listed as temporary: relational queries (`db.query`), AWS Data API drivers and views.

## Checked

Date: 2026-11-07

Confirmed against `pg/cache.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 343 lines including the Custom cache class and Limitations): defaults and strategies, Upstash setup, `$withCache` options, eventual-consistency callout, global mode, invalidation calls, both `CacheConfig` types, custom cache methods and the limitations list.

Removed: the invented Verify step. Added the limitations section and `autoInvalidate` default from the page.

Method: documentation only; no commands were run.
