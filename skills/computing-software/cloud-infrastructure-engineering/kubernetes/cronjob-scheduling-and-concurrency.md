---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cronjob-scheduling-and-concurrency
name: cronjob-scheduling-and-concurrency
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cronjob, cron-schedule, timezone, concurrencypolicy, startingdeadlineseconds, missed-schedule, successfuljobshistorylimit, failedjobshistorylimit, suspend, kubectl-create-job-from, batch-scheduling, clock-skew, create-job-from-cronjob]
level: practitioner
status: docs-checked
description: "CronJob schedule and timezone semantics, concurrencyPolicy, how missed schedules and startingDeadlineSeconds interact, history limits, suspend, and manual-trigger debugging."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#cron-job-limitations", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#time-zones", "https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CronJob scheduling and concurrency — a Job factory on a timer, with caveats

**Goal:** get a scheduled Job to run when expected, not twice, not zero times after an
outage, and understand why "it just didn't run" is usually not a bug.

## 1. Schedule and timezone
- `spec.schedule` is standard 5-field cron (`minute hour day month weekday`) with "Vixie cron" step
  values (`*/2`, `0-23/2`), `?` meaning `*`, and macros (`@yearly`/`@annually`, `@monthly`,
  `@weekly`, `@daily`/`@midnight`, `@hourly`).
- `spec.timeZone` (stable since 1.27) takes an IANA zone name (`"America/New_York"`). With no time
  zone set, the kube-controller-manager interprets schedules in its own local time zone, which is
  a classic "fired at the wrong wall-clock hour" bug after a migration. Set it explicitly even
  when it matches UTC.
- `CRON_TZ=` or `TZ=` inside `schedule` is not supported and fails validation; use `timeZone`.

## 2. concurrencyPolicy — what happens when a run is still active at the next tick
- `Allow` (default): overlapping runs both execute. Fine for idempotent, short jobs; wrong
  for anything that writes non-idempotently to a shared resource.
- `Forbid`: if the previous run has not finished when a new one is due, the new run is skipped
  (counted as missed). When the previous run finishes, `startingDeadlineSeconds` is still taken
  into account and may result in a new run.
- `Replace`: the currently running Job is replaced by a new one.
- Concurrency policy only applies to Jobs created by the same CronJob; different CronJobs always
  run concurrently.
- A job that can run long under `Forbid` can skip runs repeatedly if each run barely exceeds
  the interval; fix the runtime or widen the interval rather than switching to `Allow` without
  idempotency.

## 3. Missed schedules and startingDeadlineSeconds
The controller checks every 10 seconds, so a `startingDeadlineSeconds` below 10 may cause the
CronJob not to be scheduled. Two failure shapes:
- **Deadline**: if `startingDeadlineSeconds` is set, a Job that could not start within that many
  seconds of its scheduled time is skipped (future runs are still scheduled) and counts as
  failed. Unset means no deadline. Use it for "this report must run near 2am or not at all".
- **Too many missed**: the controller counts schedules missed since the last scheduled time (or,
  when `startingDeadlineSeconds` is set, within that window). If more than **100** were missed it
  does not start the Job and records a `TooManyMissedTimes` warning (`too many missed start times.
  Set or decrease .spec.startingDeadlineSeconds or check clock skew`). The CronJob does not stop:
  it can create a new Job later. Docs example: a one-minute schedule with the controller down for
  two hours does not start on recovery; with `startingDeadlineSeconds: 200` it still starts.
- `kubectl get cronjob <name> -o jsonpath='{.status.lastScheduleTime}'` is the first thing to
  check when a run is "missing"; compare it to the expected tick, not to now.
- CronJobs create a Job "approximately once" per execution time: occasionally two Jobs, or none.
  Make Jobs idempotent.

## 4. History, suspend, and manual runs
- `successfulJobsHistoryLimit` / `failedJobsHistoryLimit` (defaults 3 and 1) cap how many
  finished Jobs are kept; 0 keeps none, so a failing job's last run disappears unless logs are
  shipped elsewhere.
- `spec.suspend: true` stops new Jobs without affecting running ones. Runs that fall in the
  suspended period count as missed; unsuspending a CronJob that has no starting deadline
  schedules the missed Jobs immediately (subject to the 100-miss rule).
- Changes to a CronJob apply only to Jobs created afterwards; running Jobs are not updated.
- To force a run: `kubectl create job manual-run-1 --from=cronjob/<name>`. The Job is owned by the
  CronJob (ownerReference, annotation `cronjob.kubernetes.io/instantiate: manual`) but is not in
  `status.active`, so `concurrencyPolicy: Forbid` does not see it and the controller may emit an
  `UnexpectedJob` warning; a manual and a scheduled run can overlap.

## Gotchas
- The Job a CronJob creates obeys its own `backoffLimit`/`activeDeadlineSeconds` (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.job-mechanics-parallelism-and-completions`);
  a CronJob "failing" is really its child Job failing; debug there.
- The CronJob name must be at most 52 characters: the controller appends 11 characters and a Job
  name is limited to 63. Prefer DNS-label naming for predictable pod hostnames.
- From 1.32 created Jobs carry the annotation `batch.kubernetes.io/cronjob-scheduled-timestamp`
  (RFC3339, the originally scheduled time).

## Verify
- [ ] `kubectl get cronjob <name>` shows the expected `SCHEDULE`, `SUSPEND=False`, and a
      `LAST SCHEDULE` within one interval of now.
- [ ] After a long pause, the CronJob resumes on the next tick or catches up as designed by your
      `startingDeadlineSeconds`, rather than silently skipping.
- [ ] `concurrencyPolicy: Forbid` skips a tick while a Job created by the schedule is still active.
- [ ] `successfulJobsHistoryLimit`/`failedJobsHistoryLimit` match what your log retention
      can afford to lose.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the CronJob concept page: schedule syntax, step values, `?`, macros; timeZone stable 1.27 and the controller-manager local-time default; CRON_TZ/TZ unsupported (validation error); concurrencyPolicy semantics including that Forbid still honours startingDeadlineSeconds after the previous run finishes; startingDeadlineSeconds behaviour, the 10-second controller check, the 100 missed-schedule rule and the two worked examples; suspend caution; history limit defaults 3 and 1; the 52-character name limit; annotation `batch.kubernetes.io/cronjob-scheduled-timestamp` from 1.32. Kubernetes source (cronjob_controllerv2.go, utils.go): event `TooManyMissedTimes` and its message. kubectl source (create_job.go): `--from=cronjob/<name>` creates a Job with a controller ownerReference and the instantiate annotation.
Wrong in the draft and corrected: Forbid does not strictly discard skipped runs (startingDeadlineSeconds can still start one after the previous run ends); the "no deadline starts as late as noticed" wording; the claim that deleting a CronJob needs `--cascade=foreground` to remove its Jobs (removed, not documented); the name-collision remark (the limit is 52 characters).
Removed: the managed-cluster UTC remark.

Method: documentation only; no commands were run.
