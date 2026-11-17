---
id: computing-software.cloud-infrastructure-engineering.longhorn.recurring-jobs
name: recurring-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [recurring-job, cron, retain, groups, retention-policy]
level: practitioner
status: docs-checked
description: "Schedule Longhorn snapshots, backups, cleanup and trims with the RecurringJob CRD: tasks, retention policies, groups and StorageClass selectors."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/scheduling-backups-and-snapshots/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: automate snapshots, backups and maintenance.

`RecurringJob` (`longhorn.io/v1beta2`, namespace `longhorn-system`) spec fields:
- `name`: unique, 40 characters or fewer
- `task`: `backup`, `backup-force-create`, `snapshot`, `snapshot-force-create`, `snapshot-cleanup`, `snapshot-delete`, `filesystem-trim`
- `cron`: schedule
- `retain`: minimum 1, used with `count-based`
- `concurrency`: minimum 1
- `groups`, `labels`: optional
- `retentionPolicy`: `count-based` (default) or `age-based`; `retainAge` such as `720h` for age-based
- `parameters`: for backup jobs, `full-backup-interval` sets how many incrementals precede a full backup

```yaml
apiVersion: longhorn.io/v1beta2
kind: RecurringJob
metadata:
  name: nightly-backup
  namespace: longhorn-system
spec:
  task: backup
  cron: "0 2 * * *"
  retain: 7
  concurrency: 1
  groups: [default]
```

Constraints:
- `snapshot-cleanup`, `snapshot-delete` and `filesystem-trim` support only `count-based`.
- `snapshot-cleanup` ignores `retain` (set to 0).
- `age-based` with `retainAge` `0s` never runs.
- Jobs created before v1.13.0 keep `count-based`.

Groups: jobs in the `default` group apply to any volume with no recurring job. Deleting a RecurringJob removes its labels from volumes and PVCs.

StorageClass: `recurringJobSelector` is a JSON array of `{name, isGroup}` entries; volumes created from it get those jobs.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/scheduling-backups-and-snapshots/

Confirmed: name limit, tasks, retention, cron and group fields against the page.

Method: documentation only; no commands were run.
