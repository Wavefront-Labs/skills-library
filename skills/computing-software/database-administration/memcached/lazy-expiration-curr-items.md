---
id: computing-software.database-administration.memcached.lazy-expiration-curr-items
name: lazy-expiration-curr-items
category: computing-software
field: database-administration
product: memcached
tags: [curr-items, lazy-expiration, expired-unfetched, reclaimed, crawler]
level: practitioner
status: docs-checked
description: "Why curr_items does not drop when items expire: expiry is lazy, with a background thread since 1.5.0."
sources:
  - https://docs.memcached.org/userguide/faq/
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Symptom: items have expired but `curr_items` still counts them.

Cause (FAQ): expiration in memcached is lazy. An item cannot be known to be expired until something looks at it, which helps the server keep consistent performance. Since 1.5.0 a background thread analyzes the cache over time and asynchronously removes expired items from memory.

Memory is reclaimed when (Performance page): in versions prior to 1.5.0 expired items are not actively reclaimed by default; with `-o modern` on those versions, or after 1.5.0, a background thread periodically scans the cache and frees expired objects. Also, fetching an expired item makes memcached notice it is expired and free its memory, and when memory is needed the LRU tail is searched for an expired item that can be reused.

In `stats items`, `number` does not automatically exclude expired items.

Related counters (protocol.txt): `reclaimed` (times an entry was stored using memory from an expired entry), `expired_unfetched` (items pulled from the LRU that were never touched before expiring), `crawler_reclaimed` (items freed by the LRU crawler).

## Checked

2026-11-04. Confirmed against the FAQ (curr_items entry), the Performance page (When Memory Is Reclaimed) and protocol.txt (stats). Removed: the "sign of wasted sets" gloss, and the closing LRU-crawler advice (the description of the crawler is in the lru-crawler skill).

Method: documentation only; no commands were run.
