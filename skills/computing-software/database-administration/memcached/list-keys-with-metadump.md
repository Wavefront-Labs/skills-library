---
id: computing-software.database-administration.memcached.list-keys-with-metadump
name: list-keys-with-metadump
category: computing-software
field: database-administration
product: memcached
tags: [metadump, mgdump, list-keys, lru-crawler, cachedump]
level: advanced
status: docs-checked
description: "List all keys in a running instance with lru_crawler metadump or mgdump; applications must not depend on it."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/userguide/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The FAQ: you can list all keys only through a deliberately limited interface, and applications must not rely on reading all keys back. For analysis of what is stored, use the LRU crawler.

```
lru_crawler metadump <classid,classid,classid|all|hash>
lru_crawler mgdump <classid,classid,classid|all|hash>
```
- `metadump`: one line per valid item in the matching slab classes, in `key=value key2=value2` form with values URI encoded. Similar to cachedump but does not lock the cache and can return all items, not just 1MB worth. The exact keys are subject to change but include at least `key`, `exp`, `la`, `cas` and `fetch`.
- `hash` instead of a class id or `all` dumps by walking the hash table directly, which makes it more likely every item is visited once (LRU reordering and locking can cause frequently accessed items to be missed).
- `mgdump`: lines in basic metaget format like `mg key` (or `mg base64encodedkey b` for binary keys); append any flags you want and run them to fetch exactly what you want.

Replies: `OK` on successful launch, `BUSY [message]` if the crawler is already processing a request, `BADCLASS [message]` for an invalid class.

## Checked

2026-11-04. Confirmed against protocol.txt (LRU_Crawler section) and the FAQ ("How can you list all keys?"). Removed: the closing "Use cases" line (auditing TTLs, finding unused keys), which the sources do not state.

Method: documentation only; no commands were run.
