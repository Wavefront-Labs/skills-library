---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cronjob-troubleshooting-missed-schedules
name: cronjob-troubleshooting-missed-schedules
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cronjob, cronjob-troubleshooting, too-many-missed-start-times, startingdeadlineseconds, suspend, timezone]
level: practitioner
status: docs-checked
description: "Diagnose CronJobs that did not run, ran twice, or stopped: missed schedules and the 100-missed-start-times limit, startingDeadlineSeconds, suspend, time zones and concurrency."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#cron-job-limitations", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#time-zones", "https://kubernetes.io/docs/tasks/job/automated-tasks-with-cron-jobs/", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/cronjob-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CronJob troubleshooting: missed schedules

## First look
```bash
kubectl get cronjob backup -o wide            # SCHEDULE SUSPEND ACTIVE LAST SCHEDULE
kubectl get cronjob backup -o yaml            # status: lastScheduleTime, lastSuccessfulTime, active[]
kubectl get jobs --sort-by=.metadata.creationTimestamp
kubectl describe cronjob backup               # events at the bottom
kubectl create job backup-manual --from=cronjob/backup    # test the template now
```
Events the controller emits: `SuccessfulCreate`, `SawCompletedJob`, `MissSchedule` (missed its
start time or deadline), `JobAlreadyActive` (Forbid and prior run active), `TooManyMissedTimes`,
`InvalidSchedule`, `FailedCreate`, `UnexpectedJob`, `SuccessfulDelete`.

## "too many missed start times. Set or decrease .spec.startingDeadlineSeconds or check clock skew"
If the controller finds more than 100 missed schedules since the last scheduled time, it does
not start the Job and records this `TooManyMissedTimes` warning. Causes: the CronJob was
suspended for a long time, or the controller-manager was down, with a frequent schedule. The
CronJob does not stop; a later Job can still be created. Fix: set `startingDeadlineSeconds`, so
only the window of that many seconds is counted:
```yaml
spec:
  schedule: "*/5 * * * *"
  startingDeadlineSeconds: 200     # counts misses in the last 200 s; later runs start up to 200 s late
```
With a deadline set, a run that could not start within it is skipped (event `MissSchedule`).
Values below 10 seconds may stop the CronJob being scheduled, because the controller checks every 10 s.

## Other reasons a run didn't happen
| Observation | Cause |
|---|---|
| `SUSPEND True` | `spec.suspend: true` (GitOps may have re-applied it); runs in the suspended period count as missed |
| event `JobAlreadyActive` | `concurrencyPolicy: Forbid` and previous Job still running (stuck pod?) |
| Job created but no pod | quota exceeded, Pod Security admission rejection, `ImagePullBackOff`; check `kubectl describe job` events |
| ran at the "wrong" hour | with no `spec.timeZone`, the schedule uses the kube-controller-manager's local time zone; set `spec.timeZone: "Europe/London"` (stable 1.27) |
| ran twice | `concurrencyPolicy: Allow` with overlapping runs, or Job retries (`backoffLimit`); CronJobs create a Job about once per schedule time, so Jobs must be idempotent |
| old Jobs vanished | `successfulJobsHistoryLimit` (3) / `failedJobsHistoryLimit` (1), or `ttlSecondsAfterFinished` |

## Gotchas
- `CRON_TZ=` / `TZ=` inside `schedule` is not supported (validation error); use `timeZone`.
- Editing the CronJob affects only Jobs created afterwards; a running Job is unchanged.
  `Replace` policy replaces the running Job at the next schedule.
- Monitor with kube-state-metrics, for example
  `time() - kube_cronjob_status_last_successful_time > 2 * <interval>`.

## Verify
- [ ] `lastSuccessfulTime` advances each period; alert in place for staleness.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the CronJob concept page and the controller source (pkg/controller/cronjob/cronjob_controllerv2.go and utils.go): the 100 missed-schedule rule and how startingDeadlineSeconds changes the counting window, the current error text and event name `TooManyMissedTimes`, the other event reasons listed, the 10-second check interval, suspend and Forbid behaviour, time zone default and `timeZone` field (stable 1.27), unsupported CRON_TZ/TZ, history limit defaults 3 and 1, edits apply only to new Jobs. kube-state-metrics documents `kube_cronjob_status_last_successful_time`.
Wrong in the draft and corrected: the quoted error message was the old v1 wording ("Cannot determine if job needs to be started ... (> 100)"); the draft said the job is never started after the error, while the docs say the CronJob continues and can create a later Job.
Removed: a jq pipe and a grep pipe on the first-look commands.

Method: documentation only; no commands were run.
