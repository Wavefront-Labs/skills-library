---
id: computing-software.database-administration.memcached.touch-and-gat-ttl-refresh
name: touch-and-gat-ttl-refresh
category: computing-software
field: database-administration
product: memcached
tags: [touch, gat, gats, ttl-refresh, expiry-extend]
level: practitioner
status: docs-checked
description: "Refresh an item's TTL without fetching it using touch, or fetch and refresh in one step with gat, gats or mg T."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/protocols/meta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```
touch <key> <exptime> [noreply]     -> TOUCHED | NOT_FOUND
gat <exptime> <key>*                -> VALUE lines then END
gats <exptime> <key>*               -> as gat, with CAS
```
Touch replaces the existing expiry: an item with 10 s left touched with 20 expires in 20 s.

Meta equivalents:
- touch: `mg foo T30` returns `HD`.
- gat: `mg foo f v T90`; gats: `mg foo f c v T100`.

`ma` and `md` (with `I`) also accept `T`.

Stats: `cmd_touch`, `touch_hits`, `touch_misses`.

Side note: `add` on an existing key bumps it to the front of the LRU, a way to keep an item warm without reading it; if the add succeeds, it was time to recache anyway.

## Checked

Confirmed 2026-11-09: `touch`, `gat` and `gats` syntax and replies, the 10-second-left example, `mg foo T30`, `mg foo f v T90`, `mg foo f c v T100`, `T` on `ma` and `md` with `I`, stats `cmd_touch` and `touch_hits` and `touch_misses` (protocol.txt, Meta protocol page); add bumping an existing item in the LRU (Use Cases page). Nothing removed.

Method: docs-checked 2026-11-09 against memcached doc/protocol.txt and docs.memcached.org Meta protocol and Use Cases pages
