---
id: computing-software.cloud-infrastructure-engineering.velero.schedule-create-and-trigger
name: schedule-create-and-trigger
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [schedule-create, cron, velero-schedule, from-schedule, backup-schedule]
level: practitioner
status: docs-checked
description: "Create a Velero schedule from a cron expression, know the backup naming, and trigger an immediate backup from the schedule template."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a schedule with a cron expression (minute, hour, day of month, month, day of week):

```
velero schedule create example-schedule --schedule="0 3 * * *"
```

This creates the schedule within Velero, but the backup is not taken until the next scheduled time (3am here). Backups created by a schedule are saved with the name `<SCHEDULE NAME>-<TIMESTAMP>`, where the timestamp is formatted YYYYMMDDhhmmss. For the full list of flags use the CLI help:

```
velero schedule create --help
```

Trigger a backup from the schedule manually using the `velero backup` command:

```
velero backup create --from-schedule example-schedule
```

This immediately triggers a new backup based on your template for `example-schedule`. It does not affect the backup schedule: another backup triggers at the scheduled time.

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Schedule a Backup", read in full). Removed unsourced claims: the Schedule API type paragraph (`spec.template`, timeouts and their defaults, `includeClusterResources` behaviour), and the statement that backup flags become the schedule template.

Method: documentation only; no commands were run.
