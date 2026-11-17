---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.cron-execution-semantics
name: cron-execution-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [cron-at-most-once, cron-at-least-once, skipped-runs, distributed-cron, kubernetes-cronjob, idempotency]
level: advanced
status: docs-checked
description: "Choose at-most-once vs at-least-once for each scheduled job, handle skipped and overlapping runs, and configure Kubernetes CronJob concurrency, deadlines and time zone to match."
sources: ["https://sre.google/sre-book/distributed-periodic-scheduling/", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cron execution semantics

SRE Book "Distributed Periodic Scheduling with Cron": for each job, decide what failure is worse:
**skipping a launch** or **launching twice**. Garbage collection is idempotent, so launching it several
times is safe, and one skipped launch every five minutes may be acceptable. An email newsletter to a wide
distribution should not be launched more than once, and a monthly payroll job should not be skipped.
Depending on the infrastructure, you also trade off the risk of a double launch against the risk of
skipping a launch.

## Classify every job
| Job | Skip OK? | Double OK? | Semantics | Job-side safeguard |
|---|---|---|---|---|
| GC / cleanup | yes | yes | either | none |
| Daily report | no | yes (idempotent overwrite) | at-least-once | write to date-partitioned output, overwrite |
| Payroll / billing run | no | no | at-least-once + idempotent | idempotency key per period |
| Newsletter | depends | no | at-most-once | record the send per recipient |

The usual answer: **make the job idempotent and run at-least-once**; then double launches are harmless.
The book also says operations on external systems that may be continued after a leader re-election must be idempotent.

## Kubernetes CronJob knobs
```yaml
apiVersion: batch/v1
kind: CronJob
metadata: { name: daily-report }
spec:
  schedule: "17 3 * * *"
  timeZone: "Etc/UTC"
  concurrencyPolicy: Forbid          # Allow | Forbid | Replace
  startingDeadlineSeconds: 3600
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers: [{ name: report, image: registry/report@sha256:..., args: ["--date=$(RUN_DATE)"] }]
```
From the Kubernetes CronJob page:
- A CronJob creates a Job approximately once per scheduled time; two Jobs might be created, or none, so
  the Jobs you define should be idempotent.
- `startingDeadlineSeconds` is the deadline for starting a Job that missed its scheduled time; past it,
  the controller skips that execution and counts it as a failed Job. Unset means no deadline. Values under
  10 seconds may mean the CronJob is not scheduled, because the controller checks every 10 seconds.
- `concurrencyPolicy: Forbid` skips a new run if the previous is still running; `Replace` replaces the
  running Job with a new one; `Allow` permits concurrent runs.
- If more than 100 schedules were missed, the controller does not start the Job and logs an error ("too
  many missed start times"). With `startingDeadlineSeconds` set, it counts misses only in that window.
- With no `timeZone`, the kube-controller-manager uses its local time zone; set `.spec.timeZone`
  (for example `Etc/UTC`). `CRON_TZ`/`TZ` inside `schedule` are not supported.

## Skipped runs
- Alert on a job whose last success is older than a multiple of its interval (a freshness alert, not just a failure alert).
- Backfill explicitly with a parameter rather than relying on the scheduler.
- Make jobs process "everything since last successful watermark" rather than "yesterday" where possible,
  so a skipped run is absorbed by the next.

## Gotchas
- Pass the logical run date as a parameter; using `now()` inside the job breaks retries and backfills.
- `concurrencyPolicy: Allow` with long jobs can stack runs and overload dependencies.

## Verify
- [ ] Every job has documented semantics and idempotency mechanism.
- [ ] Run a job twice for the same date in staging: output unchanged, no duplicate side effects.

## Checked
2026-11-01. Confirmed against the SRE Book distributed-cron chapter (idempotent versus non-idempotent jobs,
skip versus double-launch trade-off, idempotent external operations) and the Kubernetes CronJob page (approximate-once
creation, startingDeadlineSeconds, concurrencyPolicy values, 100 missed schedules, timeZone). Removed: the claim
that Google's cron deliberately prefers skipping launches, the backoffLimit/activeDeadlineSeconds/history-limit
fields, the kube-state-metrics alert and the kubectl backfill command (not on fetched pages).
Method: documentation only; no commands were run.
