---
id: computing-software.database-administration.memcached.warm-restart-with-e-flag
name: warm-restart-with-e-flag
category: computing-software
field: database-administration
product: memcached
tags: [warm-restart, restart, e, sigusr1, persistent-memory]
level: advanced
status: docs-checked
description: "Keep the cache across clean restarts (1.5.18+) with -e memory_file on a tmpfs, graceful shutdown by SIGUSR1, and the caveats."
sources:
  - https://docs.memcached.org/features/restart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Start with `-e /tmpfs_mount/memory_file`. The mount must be a RAM disk big enough for the `-m` limit. Restart gracefully: send SIGUSR1 and wait for exit. On shutdown it writes `memory_file.meta`; on start it validates and rebuilds the hash table (seconds; 2-3 minutes near a billion items). Incompatible or corrupt files mean a clean cache.

A clean cache also results if you change: `-m`, max item size, slab chunk sizes, CAS on/off, or slab reassignment. Other options may change between restarts.

Caveats:
- System clock must be correct and must not jump while memcached is down (TTLs).
- Sets, deletes and incr/decr issued while it is down are missed: only safe if you pause/buffer updates or restart when nothing changes.
- Earliest restartable version: 1.5.18.
- Incompatible with extstore.
- A DAX persistent-memory mount works too, but this does not make memcached crash safe.

Verify: `stats settings` shows `memory_file`; check `curr_items` after restart.

## Checked

Confirmed 2026-11-09: 1.5.18 and newer, `-e` with a tmpfs path, SIGUSR1 graceful stop, `.meta` file, clean start on incompatible or corrupt files, the list of parameters that force a clean cache, clock and missed-update caveats, startup time, incompatibility with extstore, DAX mounts not being crash safe (Warm Restart page); `memory_file` in `stats settings` and `curr_items` in `stats` (protocol.txt). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Warm Restart page and memcached doc/protocol.txt
