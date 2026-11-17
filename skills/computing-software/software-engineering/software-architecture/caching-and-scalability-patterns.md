---
id: computing-software.software-engineering.software-architecture.caching-and-scalability-patterns
name: caching-and-scalability-patterns
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, caching, cache-invalidation, scalability, horizontal-scaling, read-replicas, sharding, cdn, cache-stampede, write-through, cache-aside, consistency]
level: advanced
status: draft
description: "Design a caching layer that's actually safe: invalidation strategy, stampede protection, and when to scale reads vs writes vs shard."
sources: ["Designing Data-Intensive Applications (Kleppmann) - ch. Replication, Partitioning", "Redis docs - caching patterns", "personal experience debugging stale-cache incidents"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Caching and scalability — the invalidation problem is the whole problem

**Goal:** add a cache or scale a read/write path without introducing a staleness or
stampede bug that's worse than the latency problem it solved.

## 1. "There are only two hard things in Computer Science: cache invalidation..."
Every caching decision is really an invalidation decision. Pick the strategy before
the storage:
- **TTL-based** — simplest; accept staleness up to the TTL. Fine when staleness is
  genuinely tolerable (a product listing that's a minute old is fine; an account
  balance is not).
- **Write-through/explicit invalidation** — the write path updates or deletes the
  cache entry at the same time as the DB. Correct but requires every write path
  (including batch jobs, admin tools, migrations) to go through it — a second write
  path that bypasses this is the #1 cause of "the cache says X, the DB says Y and
  nobody knows why."
- **Cache-aside** (read-through) — app checks cache, falls back to DB on miss,
  populates cache. Most common pattern; combine with a TTL as a safety net even when
  explicit invalidation exists, so a missed invalidation self-heals within the TTL
  instead of staying wrong forever.

## 2. Cache stampede ("thundering herd")
A hot key expires, and every concurrent request misses simultaneously and hits the
DB at once — the exact traffic spike the cache existed to prevent. Mitigations:
- **Request coalescing / single-flight**: only one request per key actually queries
  the DB; others wait for that result (Go's `golang.org/x/sync/singleflight`, or a
  lock in Redis).
- **Jittered TTLs**: don't expire every key from a batch load at the same instant;
  add randomized jitter (`ttl = base + random(0, base*0.1)`) so expirations spread out.
- **Stale-while-revalidate**: serve the (slightly) stale value while one request
  refreshes it in the background, rather than making every caller wait on a cold miss.

## 3. Consistency: what can be stale, and for how long
Decide explicitly, per data type, rather than applying one TTL everywhere:
- Strongly consistent reads (the user's own write must be visible immediately —
  "read your own write") need either no caching on that path, or cache keyed/bypassed
  per-session right after a write.
- Eventually consistent is fine for aggregate/derived data (counts, trending lists)
  where a few seconds of staleness has no user-visible correctness impact.

## 4. Scaling reads vs writes vs storage — different levers
- **Read-heavy**: a cache (above) or read replicas. Replicas introduce replication
  lag — a read immediately after a write can see stale data on a replica even with no
  app-level cache at all; route read-your-own-write queries to the primary.
- **Write-heavy**: a cache doesn't help writes. Options: batch writes, a write-behind
  queue (accept the write, apply async — adds eventual consistency on the read side),
  or partition the write load (sharding) so no single node absorbs all of it.
- **Data volume beyond one node**: sharding/partitioning by a key chosen for the
  actual access pattern (tenant ID for multi-tenant SaaS, user ID for user-scoped
  data) — a bad shard key (e.g. a sequential ID, or a key with one hot value like
  `tenant=default`) recreates the hotspot on one shard instead of distributing it.
- **CDN**: for static/cacheable-by-URL content, pushes the cache to the edge,
  closest to the user — the right first move for anything that's the same response
  for every user before reaching for app-level caching.

## 5. Observability for a cache, specifically
Track hit rate, not just "is the cache up" — a cache with a 5% hit rate is adding
latency and complexity for almost no benefit and the TTL/key design is wrong. Track
staleness incidents (user reports "I see old data") as a specific category, not
generic bugs — they cluster around missed invalidation paths.

## Gotchas
- Caching an error response (a 500 cached as if it were a valid result) because the
  cache layer doesn't distinguish "no value" from "failed to fetch" — cache negative
  results deliberately and briefly, never cache a failure as success.
- Serialization format changes (adding a field to a cached object's schema) without
  a cache-version bump in the key means old-format cached values get deserialized
  against new code — bump a version segment in the cache key on schema change.
- A distributed cache (Redis) as a single point of failure for a system that was
  supposed to get *more* resilient by adding a cache — plan for cache-unavailable
  behavior (fall through to DB, with a circuit breaker so a dead cache doesn't also
  take down the DB via retry storms).

## Verify
- [ ] Every write path that should invalidate a cache entry actually does, confirmed
      by testing a write via each path (including admin/batch tools) and checking
      staleness.
- [ ] A hot-key expiry was tested under concurrent load (or jitter/coalescing added)
      to rule out stampede.
- [ ] Cache hit rate is monitored; a low hit rate on a supposedly-hot cache was
      investigated, not assumed fine.
- [ ] The system degrades gracefully (falls through to source of truth) if the cache
      is unavailable, verified by actually killing it in a test environment.

Related: computing-software.software-engineering.software-architecture.choosing-architecture-styles,
computing-software.software-engineering.concurrency.profiling-before-optimising
