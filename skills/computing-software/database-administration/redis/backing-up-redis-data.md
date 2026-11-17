---
id: computing-software.database-administration.redis.backing-up-redis-data
name: backing-up-redis-data
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, rdb, aof, redis-backup, bgsave, lastsave, multi-part-aof, restore-redis, offsite-backup]
level: practitioner
status: docs-checked
description: "Back up Redis safely: copy RDB snapshots after BGSAVE completes, handle multi-part AOF directories in 7.x, ship off-host, and restore by replacing files on a stopped node."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/admin/
  - https://redis.io/docs/latest/commands/info/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up Redis

**Goal:** a restorable, off-host copy of the dataset taken without stopping Redis.

## RDB is the backup format
The RDB file is a compact point-in-time snapshot. It is never modified once produced: Redis writes
the new snapshot under a temporary name and renames it atomically when complete, so copying the file
while the server runs is safe. Procedure:
```bash
redis-cli LASTSAVE                      # unix time of last successful save
redis-cli BGSAVE                        # fork and write dump.rdb
# wait until LASTSAVE changes and INFO persistence shows rdb_bgsave_in_progress:0, rdb_last_bgsave_status:ok
cp /var/lib/redis/dump.rdb /backup/redis-$(date +%F-%H%M).rdb
```
Paths: `CONFIG GET dir` and `CONFIG GET dbfilename`. Documentation suggests hourly snapshots kept for
48 hours, daily snapshots kept for one or two months, named with date and time, and at least one
copy a day outside the data center or physical machine (for example object storage, encrypted).
After copying, check the size (and a checksum) of the transferred file. If a replica is available,
taking the snapshot there keeps the fork cost off the primary.

## AOF in Redis 7+
Since 7.0.0 the AOF is a directory (`appenddirname`, default `appendonlydir`) holding at most one
base file (RDB or AOF format), incremental files and a manifest. Copying it during a rewrite can
give an invalid backup, so:
1. `CONFIG SET auto-aof-rewrite-percentage 0` (and do not run `BGREWRITEAOF`);
2. `INFO persistence` must show `aof_rewrite_in_progress:0`;
3. copy the whole directory (hard links keep the window short);
4. `CONFIG SET auto-aof-rewrite-percentage <previous value>`.
Redis only appends to or wholesale replaces files in that directory, so hard links stay consistent.
To keep a restart from re-enabling rewrites mid-backup, also `CONFIG REWRITE` after step 1 and after
step 4. The persistence page recommends keeping RDB snapshots even when AOF is on.
Redis 8.10 adds a `BACKUP` command family (`BACKUP START`, `LIST`, `SEAL`, `CLEANUP`) and a
startup-only `preload-file` setting for restores; see the persistence page for the workflow.

## Restore
1. Stop Redis (or start a fresh instance).
2. If AOF is enabled, Redis rebuilds the dataset from the AOF at startup, not the RDB. Either restore
   the AOF directory, or set `appendonly no`, place `dump.rdb` in `dir`, start, then
   `redis-cli config set appendonly yes` (it rewrites the AOF from memory), wait for
   `aof_rewrite_in_progress` and `aof_rewrite_scheduled` to be 0 with `aof_last_bgrewrite_status:ok`,
   and persist the configuration (`CONFIG REWRITE` or edit redis.conf) or the change is lost on restart.
3. Check file ownership matches the redis user, then check the key count against the source.

## Gotchas
- A background save needs a `fork()`. Set `vm.overcommit_memory = 1` (`/etc/sysctl.conf`, then
  `sysctl vm.overcommit_memory=1`); the Redis FAQ covers fork() errors on Linux.
- While saving an RDB or rewriting the AOF, a write-heavy instance can use up to 2 times its normal
  memory (copy-on-write); size memory for it.
- Managed services use their own snapshot and export APIs instead of file copies.
- Redis Cluster: every primary shard holds part of the data, so back up each primary; the 8.10 `BACKUP START`
  can be staggered across nodes so they do not all fork at once.

## Verify
Periodically load a backup into a scratch instance (`redis-server --dir /tmp/restore --dbfilename x.rdb --port 6390`)
and compare `DBSIZE` and a few known keys.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): persistence page (snapshotting,
AOF backup, switching to AOF, BACKUP family) and administration page. Confirmed: atomic RDB rename and safe
live copy, retention suggestion, multi-part AOF layout since 7.0.0, the four-step AOF backup procedure,
hard-link note, AOF taking precedence at startup, the CONFIG SET appendonly switch procedure and its
INFO persistence checks, `vm.overcommit_memory = 1`, the 2x memory note, Redis 8.10 BACKUP commands.
Removed: the exact fork error message, the claim that an RDB from a newer version may not load in an older
one, the `redis-check-rdb` verification step, and the claim that cluster shards cannot be snapshotted
consistently (the docs do not discuss cross-shard consistency).
Method: documentation only; no commands were run.
