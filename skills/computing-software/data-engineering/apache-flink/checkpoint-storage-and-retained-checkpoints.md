---
id: computing-software.data-engineering.apache-flink.checkpoint-storage-and-retained-checkpoints
name: checkpoint-storage-and-retained-checkpoints
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, retained-checkpoints, checkpoint-storage, externalized-checkpoints, savepoint, disaster-recovery]
level: practitioner
status: docs-checked
description: "Configure Flink checkpoint storage and retention: durable storage paths, externalized checkpoints kept on cancel, how many to keep, cleanup, and restoring from one."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/checkpoints/#retained-checkpoints
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/checkpoints_vs_savepoints/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/config/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/filesystems/s3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkpoint storage and retained checkpoints

## Storage
```yaml
# config.yaml (the only supported file from Flink 2.0; flink-conf.yaml before)
execution.checkpointing.interval: 60s
execution.checkpointing.storage: filesystem          # shortcut names: 'jobmanager' (metadata and state in JobManager memory) and 'filesystem'
execution.checkpointing.dir: s3://flink-ckpt/orders-job
execution.checkpointing.savepoint-dir: s3://flink-ckpt/savepoints
execution.checkpointing.externalized-checkpoint-retention: RETAIN_ON_CANCELLATION
execution.checkpointing.num-retained: 3              # default 1
```
Layout: `<dir>/<job-id>/` holds `shared/` (state that may belong to several checkpoints), `taskowned/` (state the JobManager must never drop) and one `chk-<n>/` directory per checkpoint.

## Retention modes
- `DELETE_ON_CANCELLATION`: checkpoint state is deleted when the job is cancelled; it is kept only when the job fails.
- `RETAIN_ON_CANCELLATION`: checkpoint state is kept when the job is cancelled or fails; you clean it up manually. Consider it in production so an accidental cancel is recoverable.
- `NO_EXTERNALIZED_CHECKPOINTS`: externalized checkpoints are disabled; this is the default in the 2.3 configuration table.
Retained checkpoints are a safety net, not a replacement for savepoints: checkpoints use the state backend's native format, while savepoints are created, owned and deleted by the user and are meant for planned operations such as Flink upgrades or job graph changes.

## Restore from a retained checkpoint
```bash
flink run -s s3://flink-ckpt/orders-job/7c1e.../chk-4821 -d job.jar
```
(Use the checkpoint's metadata path, as with a savepoint; if the metadata file is not self-contained the JobManager needs access to the data files it refers to.)

Restoring a checkpoint with incremental files makes the new job reference the old job's `shared/` files. `execution.state-recovery.claim-mode` (`NO_CLAIM` default: Flink does not claim the snapshot files and takes the first checkpoint as a full one; `CLAIM`: the job takes ownership and cleans the snapshot once newer ones subsume it).

## Cleanup
- Flink keeps the newest `num-retained` completed checkpoints of a running job and discards older ones.
- Old job ids' directories from retained checkpoints accumulate: lifecycle rule on the bucket (only for job-id dirs no running job references) or a cleanup script that keeps the newest N per job.
- Never delete `shared/` of a job whose checkpoints a newer job restored from in CLAIM mode or before its first full checkpoint in NO_CLAIM mode.

## Durability
- The checkpoint storage path must be accessible from all participating processes (all TaskManagers and the JobManager), so use a distributed filesystem or object store.
- S3 entropy injection (`s3.entropy.key`, default `s3.entropy.length` 4) replaces a marker string in paths with random characters to spread S3 keys.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the generated configuration tables (`execution.checkpointing.storage|dir|savepoint-dir|num-retained|externalized-checkpoint-retention`, `execution.state-recovery.claim-mode`), the checkpoints page (retention modes, directory layout, resuming with `-s`), the checkpoints-vs-savepoints page, the S3 page (entropy) and the 2.0 configuration page (`config.yaml`). Removed the Kubernetes operator claims, the older key names, the S3 consistency claim and the stated retention default before 2.0 (the 2.3 table shows `NO_EXTERNALIZED_CHECKPOINTS`).

Method: documentation only; no commands were run.

## Verify
- [ ] Cancel a staging job; `chk-*` directories remain; restore succeeds.
- [ ] Bucket size stable over weeks (cleanup working).
