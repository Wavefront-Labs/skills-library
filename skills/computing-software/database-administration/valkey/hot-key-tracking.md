---
id: computing-software.database-administration.valkey.hot-key-tracking
name: hot-key-tracking
category: computing-software
field: database-administration
product: valkey
tags: [hotkeys, hot-keys, hotkeys-top-k, sampling, monitoring]
level: advanced
status: docs-checked
description: "Valkey hot key tracking: hotkeys-top-k, sampling-percentage, window-seconds, HOTKEYS GET/RESET, what counts as an access, and what clears state."
sources:
  - https://valkey.io/topics/hotkeys/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hot key tracking finds keys receiving disproportionate traffic, useful because a single hot key cannot be split across cluster shards. It is approximate: it samples accesses and keeps a bounded top-K list, so neither membership nor order is guaranteed.

Config (all changeable with `CONFIG SET`; changes need at least one full window to show):
- `hotkeys-top-k`: default 0 (disabled), range 0-1000; any positive value enables tracking.
- `hotkeys-sampling-percentage`: default 1, range 1-100.
- `hotkeys-window-seconds`: default 1, range 1-300.

Counts build in a live window; when it ends it is frozen and `HOTKEYS GET` reports only the last completed window. If a stall makes a window span 2x the length, live and frozen state are discarded and `GET` returns empty until the next valid window. State is per node and covers all databases in one list (entries record their database); there is no cluster-wide view.

Counted: each key lookup (hit or miss) and each removal that actually removes something, so `MGET a b c` is three accesses and `GETDEL` on an existing key is two. Not counted: replica apply stream, RDB/AOF loading, `OBJECT`, bulk slot deletion, defrag, expiration and eviction (but a client lookup triggering lazy expiry counts).

Clearing: `HOTKEYS RESET`, `FLUSHDB`, `FLUSHALL`, a full sync that empties data, cluster reset, dropping a slot. `RENAME`, `MOVE`, `SWAPDB` do not move statistics; old names age out within about 2 windows. `INFO hotkeys` summarises the last window.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/hotkeys/ (page text read in full): Sampling and top-K approximation, the three parameters with defaults and ranges, CONFIG SET, frozen-window reporting, 2x stall rule, single list across databases, per-node state, what counts and what does not, MGET and GETDEL examples, lazy-expiry exception, reset operations, rename/move/swapdb aging, INFO hotkeys.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
