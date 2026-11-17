---
id: computing-software.database-administration.redis.persistence-rdb-aof-and-durability
name: persistence-rdb-aof-and-durability
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, rdb, aof, persistence, durability, bgsave, fork, appendonly, fsync, aof-rewrite, memory-overcommit, data-loss]
level: advanced
status: docs-checked
description: "Configure Redis RDB snapshots and AOF logging so you know exactly how much data you can lose, and avoid the fork-related outage that bites under memory pressure."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis persistence: RDB, AOF, and the durability you're actually signing up for

**Goal:** know precisely how much data Redis can lose under each persistence
configuration, and avoid the specific way `BGSAVE`/AOF rewrite causes an outage
rather than just slowness.

## 1. RDB: point-in-time snapshot, not continuous
`SAVE` blocks the main thread (never run on production); `BGSAVE` forks a child
process to write the snapshot while the parent keeps serving. Triggered on
schedule (`save 900 1` etc. in redis.conf) or manually. Data loss window = time
since the last successful snapshot — a crash 10 minutes after the last save loses
everything written in those 10 minutes. Fast to restart from (single file, loads
quickly) — the usual choice when some data loss is tolerable and fast recovery
matters more.

## 2. AOF: logs every write, replayed on restart
`appendonly yes` logs each write command. `appendfsync` controls durability vs.
throughput:
- `always` — fsync every write; safest, meaningfully slower.
- `everysec` (default) — fsync once per second; loses at most ~1s of writes on a
  crash, the standard production choice.
- `no` — OS decides when to flush; can lose much more under a crash, not just a
  Redis process kill.
AOF files grow unboundedly without rewriting; `BGREWRITEAOF` (or automatic
`auto-aof-rewrite-percentage`) compacts it to the current dataset's minimal command
set, via another fork.

## 3. The fork-under-memory-pressure outage
Both `BGSAVE` and `BGREWRITEAOF` fork the process. The Redis administration page says to set
`vm.overcommit_memory = 1` (in `/etc/sysctl.conf`, or `sysctl vm.overcommit_memory=1`) and
links the FAQ entry about background saving failing with a `fork()` error on Linux. In a
write-heavy application, saving an RDB or rewriting the AOF can make Redis use up to twice its
normal memory (proportional to the pages modified during the save), so size instance memory
with headroom, not right up to capacity, and set an explicit `maxmemory`. Disable Transparent
Huge Pages too (`echo never > /sys/kernel/mm/transparent_hugepage/enabled`): with THP a fork
can trigger copy-on-write of almost the whole process memory.

## 4. Replication interacts with persistence choices
A replica with persistence disabled that restarts comes back empty and
immediately full-syncs from the primary — fine if the primary can handle a full
sync's load, risky if several replicas restart together (e.g. after a fleet-wide
reboot) and all full-sync simultaneously, saturating the primary's network/CPU.
Stagger replica restarts, or keep at least RDB enabled on replicas so they can
partial-resync instead.

## 5. Choosing a mode (or both)
The docs suggest using both RDB and AOF for data safety comparable to PostgreSQL, RDB alone if
a few minutes of loss is acceptable, and discourage AOF alone because periodic RDB snapshots
help backups, faster restarts and protect against AOF engine bugs. When both are enabled,
Redis rebuilds the dataset from the AOF at restart because it is guaranteed to be the most
complete. Know which file your restart procedure actually depends on before an incident forces
you to find out, and never enable AOF only in redis.conf on a populated instance (see the
switching-from-rdb-to-aof-at-runtime skill).

## Verify
- [ ] `appendfsync` is explicitly set (not left to assumption) and matches the acceptable data-loss window.
- [ ] `vm.overcommit_memory = 1` on hosts running BGSAVE/BGREWRITEAOF under meaningful write load.
- [ ] Instance memory has headroom above dataset size for a fork's worst-case COW growth.
- [ ] A real restart was tested and confirmed it loads from the expected file (AOF vs RDB).
- [ ] Replica restarts are staggered, or replicas retain enough persistence to avoid simultaneous full syncs.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the persistence and administration pages: RDB is a point-in-time snapshot made by a forked child; SAVE blocks all clients and BGSAVE is preferred; AOF with appendfsync always, everysec (default, about one second lost) and no; automatic AOF rewrite; Redis 7.0 multi-part AOF; when both are enabled the AOF is used at restart; RDB lets replicas partially resync after restarts; `vm.overcommit_memory = 1` and Transparent Huge Pages disabled; up to 2x memory during a save or rewrite in write-heavy workloads; a replica restarted from an empty state does a full sync. Removed unconfirmed: the exact fork error text, the claim that background persistence is silently disabled, and a fallback from AOF to RDB.
Method: documentation only; no commands were run.
