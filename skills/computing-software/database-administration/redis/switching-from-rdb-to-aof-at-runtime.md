---
id: computing-software.database-administration.redis.switching-from-rdb-to-aof-at-runtime
name: switching-from-rdb-to-aof-at-runtime
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, rdb, aof, appendonly-runtime, config-set, persistence, durability]
level: practitioner
status: docs-checked
description: "Enable AOF on a running Redis without losing data: CONFIG SET appendonly yes, waiting for the rewrite, persisting the change, and pitfalls of editing redis.conf alone."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/#how-i-can-switch-to-aof-if-im-currently-using-dumprdb-snapshots
  - https://redis.io/docs/latest/commands/config-rewrite/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switching from RDB to AOF at runtime

## The trap
If you add `appendonly yes` to redis.conf and restart, Redis starts with an **empty AOF** and
loads from it (AOF takes priority over RDB when enabled), so the dataset appears **empty**.
The persistence docs warn that not following the live-switch procedure (for example just changing the config and restarting) can result in data loss. Do not do that.

## Safe procedure (Redis 7.x)
```bash
redis-cli BGSAVE                         # fresh RDB as a safety net; wait for it:
redis-cli INFO persistence | grep -E 'rdb_bgsave_in_progress|rdb_last_bgsave_status'
cp /var/lib/redis/dump.rdb /backup/dump.rdb.$(date +%F)

redis-cli CONFIG SET appendonly yes      # starts an AOF rewrite from the in-memory dataset
redis-cli INFO persistence | grep -E 'aof_rewrite_in_progress|aof_rewrite_scheduled|aof_last_bgrewrite_status'
```
Wait until `aof_rewrite_in_progress:0` and `aof_last_bgrewrite_status:ok`; the `appendonlydir/`
now holds a base file with the full dataset plus incremental files.

Persist the setting so a restart keeps AOF on:
```bash
redis-cli CONFIG REWRITE                 # rewrites redis.conf with current settings
# or edit redis.conf: appendonly yes, appendfsync everysec
```
Check the config file afterwards; managed config (Ansible, Helm) must be updated too or the
next deploy turns AOF off again.

## Choosing settings
```
appendonly yes
appendfsync everysec                 # balance; 'always' = fsync per write (slow), 'no' = OS decides
aof-use-rdb-preamble yes             # base file in RDB format: faster rewrite and load
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```
Keeping RDB snapshots (`save` points) as well gives compact backups; both can be on.

## Switching back to RDB-only
`CONFIG SET appendonly no` stops AOF; make sure an RDB save exists (`BGSAVE`) before removing
the AOF directory.

## Gotchas
- The rewrite forks: needs memory headroom (copy-on-write) and `vm.overcommit_memory = 1`.
- Replicas: set it on each node; a replica's persistence is independent.
- Kubernetes/containers: the AOF directory must be on the persistent volume.

## Verify
After a controlled restart, `DBSIZE` matches pre-restart and `INFO persistence` shows
`aof_enabled:1`, `loading:0`.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the persistence page: enable AOF on the live server with `CONFIG SET appendonly yes` after backing up dump.rdb, optionally `CONFIG SET save ""`, wait for `aof_rewrite_in_progress` and `aof_rewrite_scheduled` to be 0 and `aof_last_bgrewrite_status` ok, update redis.conf (CONFIG REWRITE) or the change is lost on restart, then check the key count; when both RDB and AOF are enabled the AOF is used at restart; Redis 7.0 multi-part AOF directory with base and incremental files; appendfsync always/everysec/no. Confirmed from redis.conf (8.2): `aof-use-rdb-preamble yes`, `auto-aof-rewrite-percentage 100`, `auto-aof-rewrite-min-size 64mb`, everysec default. Confirmed from the administration page: switching between AOF and RDB at runtime with CONFIG SET and overcommit advice. INFO fields confirmed. Removed the unconfirmed server log message and the claim about the next RDB save.
Method: documentation only; no commands were run.
