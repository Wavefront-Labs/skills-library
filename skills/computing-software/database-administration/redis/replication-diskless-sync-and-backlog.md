---
id: computing-software.database-administration.redis.replication-diskless-sync-and-backlog
name: replication-diskless-sync-and-backlog
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-replication, diskless-replication, repl-backlog, replicaof, partial-resync, psync, repl-diskless-sync, replica-read-only]
level: practitioner
status: docs-checked
description: "Run Redis primary/replica replication well: REPLICAOF, partial resync and repl-backlog-size, diskless sync, and diagnosing full-resync loops."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/replication/
  - https://raw.githubusercontent.com/redis/redis/unstable/redis.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replication config, diskless sync, backlog

**Goal:** replicas that resync partially after blips instead of doing expensive full syncs, and full syncs that do not hammer disks.

## Set up
```text
# replica redis.conf
replicaof 10.0.0.5 6379
masterauth <password>          # or masteruser + masterauth with ACLs
replica-read-only yes
replica-serve-stale-data yes   # serve (stale) data while the link is down or syncing; no = replicas reply with an error
```
Runtime: `REPLICAOF 10.0.0.5 6379`; promote: `REPLICAOF NO ONE`.

## Partial vs full resync
Each replica tracks (replication ID, offset). After a disconnect, it asks `PSYNC id offset`; if that offset is still in the primary's **backlog**, only the missing stream is sent. Otherwise: full resync (fork, RDB, transfer, load).
```text
repl-backlog-size 256mb        # default 1mb; size it to your write rate (see below)
repl-backlog-ttl 3600          # free backlog after no replicas for N s
```
Size it = write bytes/sec x longest disconnect to survive (e.g. 2 MB/s x 120 s = 240 MB). Check `INFO replication`: `master_repl_offset`, `repl_backlog_histlen`; `INFO stats`: `sync_full`, `sync_partial_ok`, `sync_partial_err`.

## Diskless sync
```text
repl-diskless-sync yes         # default yes since 7.0: stream RDB over the socket, no disk write on primary
repl-diskless-sync-delay 5     # wait for more replicas to batch one transfer
repl-diskless-load on-empty-db # replica; default is disabled; swapdb keeps the old data in RAM (OOM risk)
```
Use when disk is slow (cloud volumes) and network fast.

## Full-resync loop
Symptom: replica repeatedly syncs; the primary closes the replica connection. Likely cause: the replication buffer during RDB transfer exceeded
```text
client-output-buffer-limit replica 256mb 64mb 60
```
Raise it (e.g. `1gb 512mb 120`) and the backlog; ensure transfer finishes before the limit.

## Gotchas
- Primary with persistence off + auto restart = it comes back empty and replicas sync the empty dataset: disaster. Persist on primary or disable auto restart.
- Replicas expire keys only when the primary sends DELs; reads on replicas hide logically expired keys.
- Writes to a replica (`replica-read-only no`) are local and lost on resync.

## Verify
`INFO replication` on replica: `master_link_status:up`, small `master_last_io_seconds_ago`; restart the replica process and `sync_partial_ok` increments on the primary, not `sync_full`.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the replication page, administration page and redis.conf: replicas ask `PSYNC` with replication ID and offset and fall back to a full resync when the backlog cannot serve them; `repl-backlog-size` default 1mb and `repl-backlog-ttl` 3600; `repl-diskless-sync` default yes in 7.0 (no in 6.0), `repl-diskless-sync-delay` 5, `repl-diskless-load` default disabled with on-empty-db and swapdb; `client-output-buffer-limit replica 256mb 64mb 60`; `replicaof ... / REPLICAOF NO ONE`; `masterauth`/`masteruser`; `replica-read-only` default yes and writable-replica writes discarded on resync; replicas wait for the primary's DEL and hide expired keys on reads; a primary restarting empty wipes replicas; INFO fields `sync_full`, `sync_partial_ok`, `sync_partial_err`, `repl_backlog_histlen`, `master_link_status`. Removed unconfirmed: the -MASTERDOWN error name, the exact primary log message, the 3.2 version tag.
Method: documentation only; no commands were run.
