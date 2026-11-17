---
id: computing-software.data-engineering.apache-flink.state-backends-and-savepoints
name: state-backends-and-savepoints
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, state-backend, rocksdb, hashmapstatebackend, savepoint, checkpoint, incremental-checkpoint, state-ttl, keyed-state, operator-state, state-migration, job-upgrade, flink-sql, changelog-state-backend]
level: practitioner
status: docs-checked
description: "Choose RocksDB vs heap state backends, size state, and use savepoints/checkpoints safely for upgrades and recovery."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink state backends, savepoints and safe upgrades

**Goal:** keep a job's state small enough and durable enough to checkpoint fast, and upgrade/restart jobs without losing or corrupting it.

## 1. HashMapStateBackend vs RocksDB — pick by state size, not habit
- **HashMapStateBackend**: state lives as Java objects on heap. Fastest access, but bounded by JVM heap and subject to GC pauses as state grows — fine when per-key state is small and total state fits comfortably in heap (roughly: state << configured heap).
- **EmbeddedRocksDBStateBackend**: state lives off-heap in RocksDB (serialized bytes), spilling to local disk. Handles state far larger than RAM, but every access pays (de)serialization cost — meaningfully slower per-record than heap for small state. Choose it once state could exceed available heap.
- **Gotcha:** switching backend between runs is not just a config flag at restore time for incompatible state representations — check compatibility before changing backend and restoring from an old savepoint; test on a non-prod job first.
- RocksDB tuning that actually matters: `state.backend.rocksdb.memory.managed` (active by default per the Flink docs) bounds RocksDB's native memory inside Flink's managed memory; set it to `false` only if you tune RocksDB memory manually.

## 2. Checkpoints vs savepoints — different purposes, same mechanism
- **Checkpoint**: automatic, periodic, owned by Flink, used for failure recovery. Incremental checkpoints (RocksDB only) upload only changed SST files since the last checkpoint — dramatically cheaper than full snapshots for large state; enable via `execution.checkpointing.incremental: true` (the key in the Flink state backends docs).
- **Savepoint**: manually triggered, self-contained, portable snapshot for deliberate operations — job upgrades, scaling the parallelism, migrating clusters. `flink stop --savepointPath s3://.../sp1 <job-id>` stops the job *and* takes a savepoint atomically; `flink savepoint <job-id> s3://...` takes one without stopping.
- Never treat a checkpoint directory as a savepoint for a planned restart — checkpoints can be pruned/incremental and aren't guaranteed self-contained the way savepoints are; always savepoint before any deliberate stop you intend to resume from.

## 3. Upgrading a running job without losing state
1. Ensure every stateful operator has an explicit **`uid()`** set. Without it, Flink auto-generates uids from the topology; reordering/adding operators shifts the auto-generated ids and state silently fails to restore (or restores into the wrong operator) on the next deploy.
2. `flink stop --savepointPath ... <job-id>` the old job.
3. Deploy new JAR, `flink run -s <savepoint-path> ...` to restore state into matching uids. New operators with no matching uid start with empty state (fine if intentional); if you expected state to carry over and it didn't, check the uid matched.
4. **State schema evolution**: POJO/Avro state schema changes (added/removed fields) are supported for savepoint restore if the serializer supports schema evolution (Flink's POJO serializer does for simple cases; custom `TypeSerializer`s often don't). Test restore with the new schema against a real savepoint before shipping — a failed restore with no fallback is a data-loss incident.

## 4. State TTL
`StateTtlConfig` expires keyed state after inactivity (idle/last-update based). Essential for unbounded-key streams (e.g. per-session state) to stop state size growing forever. `cleanupInRocksdbCompactFilter()` reclaims RocksDB disk during compaction instead of only logical expiry, which matters because logical-only expiry still leaves bytes on disk until compaction happens anyway.

## Verify
- [ ] Every stateful operator has an explicit `.uid("...")`.
- [ ] A savepoint-then-restore cycle on a staging job preserves exact state content (spot-check a few keys).
- [ ] Checkpoint duration stays well under the checkpoint interval (checkpoints queuing up behind each other means backpressure incoming).
- [ ] RocksDB-backed job's container memory includes headroom beyond `state.backend.rocksdb.memory.managed` allocation — no OOM-kills under load.
- [ ] State TTL is configured for any keyed state on an unbounded key space (sessions, user ids).

## Checked

2026-10-28. Confirmed: execution.checkpointing.incremental and state.backend.rocksdb.memory.managed (default active) on the state backends page. Removed: a WRONG incremental-checkpoint key (`state.backend.incremental`), a claim that RocksDB is the default, a superlative about incidents and a version note.

Method: documentation only; no commands were run.
