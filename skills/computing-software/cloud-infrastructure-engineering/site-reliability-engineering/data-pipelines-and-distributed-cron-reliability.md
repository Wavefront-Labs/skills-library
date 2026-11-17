---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.data-pipelines-and-distributed-cron-reliability
name: data-pipelines-and-distributed-cron-reliability
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, data-pipelines, pipeline-reliability, batch-pipelines, streaming-pipelines, distributed-cron, cron-reliability, scheduled-jobs, periodic-jobs, idempotency, exactly-once, at-least-once, checkpointing, backfill, replay, dead-letter-queue, freshness-slo, correctness-slo, completeness, data-slo, pipeline-monitoring, airflow, argo-workflows, kubernetes-cronjob, concurrency-policy, missed-runs, thundering-herd, hot-spots, dataflow]
level: advanced
status: docs-checked
description: "Run batch/streaming pipelines and scheduled jobs reliably: freshness/correctness/completeness SLOs for data, idempotent checkpointed stages, and cron launch tracking."
sources: ["https://sre.google/sre-book/data-processing-pipelines/", "https://sre.google/workbook/data-processing/", "https://sre.google/sre-book/distributed-periodic-scheduling/", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/", "https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data pipelines and distributed cron reliability

**Goal:** pipelines that deliver data on time and correct, can be re-run safely when they
fail, and scheduled jobs that run exactly as often as intended even when schedulers,
nodes or regions fail.

## 1. SLOs for data (SRE Workbook)
Measure the pipeline the way its consumers experience it:
- **Freshness**: age of the newest data at the output (`time() − last_successful_run_end`
  or watermark lag); the Workbook gives freshness SLO formats for pipeline output.
- **Correctness**: outputs passing invariants you define (sums reconcile, no nulls in keys,
  schema matches); the Workbook also describes backward-looking correctness targets.
- **Coverage/completeness**: fraction of input records/partitions processed (dropped =
  dead-lettered + lost).
Export them as metrics from the pipeline itself and alert on the SLO, not on "task failed"
(a failed task that retries within SLO is not an incident).

## 2. Pipeline design rules
- **Idempotent stages**: re-running stage N for partition P produces the same output and
  overwrites, not appends (write output atomically, upsert by record id, dedupe downstream).
  The Workbook's idempotent mutation pattern: same input always gives the same result.
- **Checkpoint and replay**: jobs checkpoint progress so a restart or reschedule skips finished work
  units (Workbook, Checkpointing); keep replay a documented, tested procedure.
- **Dead-letter path**: malformed records go to a DLQ with the error, never silently dropped
  and never block the stream; alert on DLQ rate.
- **Backpressure and isolation**: bound in-flight work; separate queues/workers per tenant
  or per priority; one bad tenant's backlog must not delay everyone.
- **Schema evolution**: versioned schemas (Avro/Protobuf with a registry), compatibility
  rules enforced in CI; consumers tolerate unknown fields.
- **Backfills**: a separate, rate-limited path with its own quota so a 90-day reprocess does
  not starve the live pipeline; mark backfill writes for audit.
- **Multi-phase pipelines** (A→B→C): each phase has its own SLO and each phase's output feeds the next, so phase delays add up; periodic pipelines suit infrequent work; for continuous work the SRE Book
  describes Google Workflow: a Task Master (writer elected through Chubby) holds work units, and
  workers may commit only work whose lease they hold (`...site-reliability-engineering.distributed-consensus-for-critical-state`).

## 3. Failure modes to design out (SRE Book)
| Failure | Looks like | Fix |
|---|---|---|
| **Hot spots** | an overloaded resource or key range delays isolated parts of the data | see the Workbook's hotspotting strategies |
| **Thundering herd** | many pipeline workers or jobs start together and hit shared infrastructure | spread start times, rate limit shared stores |
| **Moiré load pattern** | two or more pipelines' runs overlap and together overload a shared resource | stagger runs, model aggregate load |
| **Unbounded retries** | failed partition retried forever, blocking later ones | retry budget per partition, then DLQ + alert |
| **Silent partial failure** | job "succeeds" with half the records | completeness checks and reconciliation |
| **Resource starvation by backfill** | live pipeline late during reprocessing | separate quotas/queues |

## 4. Distributed cron: semantics first
Decide per job: **at-least-once** (safe to double-run; idempotent) or **at-most-once**
(must never double-run; may skip). Most jobs should be made idempotent so at-least-once is fine.
- A single cron host is a SPOF and loses runs during its outage; distributed cron needs a
  **leader** (consensus-elected) that records launched runs in replicated state, so a new
  leader knows which runs happened. Google's cron keeps launch state in Paxos with a single leader that is the only replica launching jobs;
  Kubernetes docs warn a CronJob may occasionally create two Jobs or none, so Jobs should be idempotent.
- **Missed runs policy**: after an outage, run once (catch up) or skip? Kubernetes:
  `startingDeadlineSeconds` (how late a run may start, else that run is skipped); with more than 100
  missed schedules the controller does not start the Job and logs an error; `concurrencyPolicy` is
  `Allow` (default), `Forbid` or `Replace`.
- **Launch tracking**: write "launching run R" before launching, "launched" after; on
  leader change, a run in "launching" state is ambiguous → policy decides (re-run if idempotent).
- **Time zones and DST**: schedule in UTC or set `timeZone` explicitly (Kubernetes ≥ 1.27
  `spec.timeZone: Europe/London`); DST makes 02:30 happen twice or never.
- Large fleets: avoid every machine's cron hitting shared services at the same minute.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata: { name: nightly-export }
spec:
  schedule: "17 2 * * *"                 # not :00 — spread load
  timeZone: Etc/UTC
  concurrencyPolicy: Forbid               # at-most-one-running; Replace kills the old run
  startingDeadlineSeconds: 3600           # catch up within 1h, else count as missed
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 5
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: export
              image: registry/export:1.4.2
              args: ["--partition=$(date -u +%F)", "--idempotent"]
```
Alert on a per-job freshness metric pushed from the job, not only on Job failures.

## 5. Orchestrators (Airflow)
- Airflow: `catchup` defaults to False (`scheduler.catchup_by_default`); set True only when running every
  missed interval is intended; backfill re-runs a chosen historical period.
- Make tasks idempotent per partition or data interval; use sensor timeouts, not infinite waits.

## 6. Operate
Dashboards: freshness per output, run duration trend (creeping toward the window = future
incident), records in/out/DLQ per stage, backlog/consumer lag,
worker utilisation and skew (max/median task duration). Runbooks: replay partition,
pause consumer, drain DLQ, promote scheduler.

## Gotchas
- "Exactly-once" claims usually mean effectively-once within one system; crossing a system boundary (DB → Kafka → HTTP) needs idempotent sinks.
- Non-idempotent jobs with `concurrencyPolicy: Allow` and a slow run → overlapping writes.
- Cron catch-up after a long outage launching 100 runs at once; set a deadline and a catch-up policy.
- Pipelines that only alert on task failure and not on freshness miss a scheduler that never ran.
- A backfill run with the live path's default limits can overload the source database.

## Verify
- [ ] Each pipeline exports freshness/completeness/correctness metrics and has an SLO-based alert; task-failure alerts are tickets, not pages.
- [ ] Re-running yesterday's partition twice yields identical outputs (checksum) and no duplicates downstream.
- [ ] Killing the scheduler leader during a schedule tick results in exactly one run (idempotent at-least-once) or a logged skip (at-most-once), per the job's policy.
- [ ] A 7-day backfill completed without the live pipeline missing its freshness SLO.

## Checked
2026-11-01. Confirmed in the SRE Book (Data Processing Pipelines; Distributed Periodic Scheduling with Cron), the SRE Workbook Data Processing chapter, the Kubernetes CronJob page and the Airflow DAG run page: thundering herd, Moire load pattern, Workflow leases and Chubby-elected Task Master, Paxos cron leader and launch tracking, cron idempotency, freshness and correctness SLOs, idempotent mutations, checkpointing, hotspotting, `startingDeadlineSeconds`, 100-missed-schedule behaviour, `concurrencyPolicy` values, `timeZone`, history limits, Airflow catchup. Removed: metric names, Kafka/Flink/Argo/Dagster/Prefect specifics, Airflow multi-scheduler and SLA claims, etcd statement, Job backoff/deadline/TTL fields, example SLO figures.
Method: documentation only; no commands were run.
