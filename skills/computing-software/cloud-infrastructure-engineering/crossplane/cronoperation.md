---
id: computing-software.cloud-infrastructure-engineering.crossplane.cronoperation
name: cronoperation
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [cronoperation, schedule, concurrency, operations]
level: advanced
status: docs-checked
description: "Schedule recurring Operations with CronOperation: cron syntax, concurrency, history and deadlines."
sources:
  - https://docs.crossplane.io/latest/operations/cronoperation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `CronOperation` creates Operations on a schedule like a CronJob. It is alpha and needs `--enable-operations`.

```yaml
apiVersion: ops.crossplane.io/v1alpha1
kind: CronOperation
metadata:
  name: daily-backup
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  successfulHistoryLimit: 5
  failedHistoryLimit: 3
  startingDeadlineSeconds: 900
  operationTemplate:
    spec:
      mode: Pipeline
      pipeline:
      - step: backup
        functionRef:
          name: function-database-backup
```

Fields:

- `schedule` is standard five-field cron, for example `*/15 * * * *` or `0 9 * * 1-5`.
- `concurrencyPolicy`: `Allow` (default), `Forbid` (skip while a previous run is going) or `Replace` (stop the running one).
- `successfulHistoryLimit` and `failedHistoryLimit` bound retained Operations.
- `startingDeadlineSeconds`: if the Operation cannot start within this window of its scheduled time, that run is skipped.

Time uses the cluster's local time zone, so standardize on UTC and account for DST.

Status shows `lastScheduleTime`, `lastSuccessfulTime`, `runningOperationRefs` and a `Scheduling` condition.

Pick `Forbid` for jobs that must not overlap, such as backups, and `Replace` when only the newest run matters.

## Checked

2026-11-08: read the whole Crossplane Cron Operations guide (raw source of docs.crossplane.io/latest/operations/cronoperation). Confirmed the alpha flag, the example manifest fields, five-field cron syntax, the three concurrency policies and the Allow default, history limits, `startingDeadlineSeconds` skip behaviour, the local time zone and DST warning, and the status fields and `Scheduling` condition.
Method: documentation only; no commands were run.
