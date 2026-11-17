---
id: computing-software.systems-network-administration.backup-and-recovery.redis-rdb-and-aof-backups
name: redis-rdb-and-aof-backups
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [redis-persistence-backup, redis, rdb, aof, database-backup, in-memory-database]
level: practitioner
status: docs-checked
description: "Back up Redis safely: RDB snapshots with BGSAVE, multi-part AOF directories in Redis 7, copying files while running, and restoring without the AOF overriding the RDB."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://redis.io/docs/latest/commands/bgsave/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis RDB and AOF backups

**Goal:** restorable Redis backups that do not block production.

## Persistence modes
- **RDB**: point-in-time snapshot `dump.rdb`, written by a forked child (`save 3600 1 300 100 60 10000` rules, or `BGSAVE`).
- **AOF**: append log of writes (`appendonly yes`, `appendfsync everysec`). Redis 7+ uses multi-part AOF: a directory (`appenddirname`, default `appendonlydir`) with a base file, incremental files and a manifest.
- Both on is common: AOF for durability, RDB for backups.

## Back up RDB
```sh
redis-cli BGSAVE
until redis-cli INFO persistence | grep -q 'rdb_bgsave_in_progress:0'; do sleep 2; done
redis-cli INFO persistence | grep rdb_last_bgsave_status   # must be ok
cp /var/lib/redis/dump.rdb /backup/redis-$(date +%F-%H%M).rdb
```
The RDB is written to a temp file and renamed atomically, so copying it any time is safe.

## Back up AOF (Redis 7+)
Prevent a rewrite during the copy, then copy the whole `appenddirname` directory (default `appendonlydir`):
```sh
redis-cli CONFIG GET auto-aof-rewrite-percentage          # note the current value
redis-cli CONFIG SET auto-aof-rewrite-percentage 0
redis-cli INFO persistence | grep aof_rewrite_in_progress:0
cp -a /var/lib/redis/appendonlydir /backup/aof-$(date +%F)
redis-cli CONFIG SET auto-aof-rewrite-percentage <previous-value>
```
Do not run `BGREWRITEAOF` during the copy. Hard-linking the files first lets you re-enable rewrites sooner. To survive a restart mid-backup, persist the setting with `CONFIG REWRITE` (and again when re-enabling). Before Redis 7.0.0 the AOF is a single file that can simply be copied.

## Online backups with BACKUP (newer Redis)
The current Redis documentation describes a `BACKUP` command family (documented as available since Redis 8.10.0; check your version): `BACKUP START` produces a fresh BASE snapshot, `BACKUP LIST` reports the files to copy, `BACKUP SEAL` freezes the backup and writes a manifest, and `BACKUP CLEANUP` releases the files after copying. Files go to the `backupdirname` directory (default `backupdir`). Restore by pointing the startup-only `preload-file` setting at the manifest (`preload-file aof:<path>/appendonly.aof.manifest`) or at an RDB (`preload-file rdb:<path>`).

## Restore
1. Stop Redis.
2. Put `dump.rdb` (or the AOF dir) in `dir` with the right owner.
3. **If both RDB and AOF are enabled, Redis uses the AOF to rebuild the dataset because it is guaranteed to be the most complete.** To restore from an RDB, start with `appendonly no`, then `CONFIG SET appendonly yes` and persist the change in `redis.conf` (for example with `CONFIG REWRITE`); the manual warns that skipping the config update loses data on restart, and that you should wait for `aof_rewrite_in_progress` and `aof_rewrite_scheduled` to reach 0 and check `aof_last_bgrewrite_status` before restarting.
4. Start and check `DBSIZE` and key samples.

## Gotchas
- BGSAVE forks a child, so the Redis admin guide recommends setting the Linux kernel `vm.overcommit_memory = 1`.
- Redis Cluster: take a backup from every shard.
- Managed Redis services use their own snapshot and export features; check the provider documentation.

## Verify
Restore the latest RDB into a scratch instance and compare `DBSIZE` and a few known keys.

## Checked

Checked 2026-10-27 against the Redis documentation sources in redis/docs (persistence, admin, INFO and BGSAVE pages) and the default redis.conf in redis/redis. Confirmed: atomic rename of RDB files so copies are safe, the multi-part AOF directory since 7.0.0 with `appenddirname` default `appendonlydir`, the AOF backup procedure with `auto-aof-rewrite-percentage 0` and restoring the previous value, `CONFIG REWRITE` persistence, the AOF being preferred when both are enabled, the safe switch-to-AOF procedure, the INFO fields `rdb_bgsave_in_progress`, `rdb_last_bgsave_status` and `aof_rewrite_in_progress`, `vm.overcommit_memory = 1`, and the `BACKUP` command family with `backupdirname` and `preload-file` as documented there.
Method: documentation only; no commands were run.
