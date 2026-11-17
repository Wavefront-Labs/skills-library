---
id: computing-software.database-administration.memcached.inspect-running-config-stats-settings
name: inspect-running-config-stats-settings
category: computing-software
field: database-administration
product: memcached
tags: [stats-settings, stats, running-config, verify, nc]
level: practitioner
status: docs-checked
description: "Confirm what memcached is actually running with using stats settings and stats, including defaults like maxconns 1024."
sources:
  - https://docs.memcached.org/serverguide/configuring/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Never trust the init script alone. Ask the daemon:

```
echo "stats settings" | nc localhost 11211
```
Sample keys (docs defaults): `maxbytes 67108864`, `maxconns 1024`, `tcpport 11211`, `num_threads 4`, `cas_enabled yes`, `tcp_backlog 1024`, `item_size_max 1048576`, `growth_factor 1.25`, `chunk_size 48`.

protocol.txt also lists `slab_reassign`, `slab_automove`, `lru_crawler`, `lru_maintainer_thread`, `temp_lru`, `idle_time`, `track_sizes`, `memory_file`, `proxy_enabled`, and `ssl_`-prefixed TLS settings.

Caveats: output order is not guaranteed, the list is not exhaustive and it is subject to change between versions.

Use `stats` (counters) and `stats settings` together to check that what you asked for matches what runs, for example `limit_maxbytes` for -m.

## Checked

2026-11-04. Confirmed against the Configuring page (stats settings sample and defaults) and protocol.txt (settings table, ordering and exhaustiveness caveat). Removed: nothing.

Method: documentation only; no commands were run.
