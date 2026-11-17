---
id: computing-software.data-engineering.apache-flink.flink-cli-operations
name: flink-cli-operations
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-cli, flink-run, stop-with-savepoint, flink-list, flink-cancel, savepoint, job-operations]
level: practitioner
status: docs-checked
description: "Operate Flink jobs from the CLI and REST: run with savepoint and parallelism, list, stop-with-savepoint vs cancel, trigger and dispose savepoints, and allowNonRestoredState."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/cli/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/rest_api/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/savepoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink CLI operations

**Goal:** routine job lifecycle on session/standalone/YARN clusters (and to understand what the k8s operator does underneath).

## Submit
```bash
flink run -d -p 8 -c com.acme.OrdersJob orders-job.jar --env prod          # detached
flink run -d -s s3://chk/savepoints/savepoint-ab12 -p 12 orders-job.jar     # restore from savepoint
flink run -d -s <path> --allowNonRestoredState orders-job.jar               # skip state of removed operators
flink run -t yarn-application -Djobmanager.memory.process.size=2g orders-job.jar
flink run -t kubernetes-application -Dkubernetes.cluster-id=orders local:///opt/flink/usrlib/orders-job.jar
```
`--allowNonRestoredState` (short `-n`) is needed when an operator with state was removed; without it the restore fails so you do not lose state by accident.

## Inspect
```bash
flink list                    # running/scheduled jobs with IDs
flink info orders-job.jar     # execution plan of a job
```

## Stop vs cancel
```bash
flink stop --savepointPath s3://chk/savepoints/ <jobId>           # savepoint then graceful stop (sources stop, sinks commit)
flink stop --drain --savepointPath s3://chk/savepoints/ <jobId>   # also emit MAX_WATERMARK: fires all timers/windows (use only for final shutdown)
flink cancel <jobId>                                                # no savepoint; ungraceful, use stop instead where possible
```
`--drain` emits a `MAX_WATERMARK` before the final checkpoint, so event-time windows fire as if the stream ended. Use it only to terminate a job permanently; do not drain if the job will be resumed.

## Savepoints
```bash
flink savepoint <jobId> s3://chk/savepoints/              # trigger while running
flink savepoint --type native <jobId>                      # native format (default is canonical)
flink savepoint --dispose s3://chk/savepoints/savepoint-ab12
```
REST equivalents: `POST /jobs/:id/savepoints` (body fields `target-directory`, `cancel-job`, `formatType`), `POST /jobs/:jobid/stop` (body fields `targetDirectory`, `drain`, `formatType`); both return a `triggerid` to poll.

## Restoring from a retained checkpoint
With `execution.checkpointing.externalized-checkpoint-retention: RETAIN_ON_CANCELLATION`, `flink run -s s3://chk/<jobId>/chk-1234 ...` restores from a checkpoint (a checkpoint is used like a savepoint by passing its metadata path).

## Gotchas
- Savepoint paths must be reachable by JobManager and TaskManagers (shared storage).
- Detached submit returns before the job is running; check `flink list` or REST for state.
- Without explicit `uid()` on operators, IDs are assigned from the topology, so job graph changes can map state to the wrong operators or fail the restore. Set uids before the first prod deploy.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the CLI page (run/list/info/cancel/stop, `--drain`, `--allowNonRestoredState`, `savepoint --dispose`), the savepoints page (`--type [native/canonical]`, `uid()`), and the generated REST API table for `POST /jobs/:jobid/savepoints` and `POST /jobs/:jobid/stop`. Removed the unconfirmed `flink list -a` flag, version gate and error string.

Method: documentation only; no commands were run.

## Verify
- [ ] Upgrade runbook: stop with savepoint -> deploy -> run -s; tested in staging.
- [ ] Savepoint retention and disposal policy defined (they are not auto-deleted).
