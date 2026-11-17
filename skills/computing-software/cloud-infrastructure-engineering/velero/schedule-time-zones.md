---
id: computing-software.cloud-infrastructure-engineering.velero.schedule-time-zones
name: schedule-time-zones
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [cron-tz, time-zone, daylight-saving, schedule-timezone, iana]
level: practitioner
status: docs-checked
description: "Pin a Velero schedule to a time zone with CRON_TZ and avoid daylight-saving surprises, including the skipped-run caveat."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To pin a Velero schedule to a zone, prefix the cron expression with `CRON_TZ=<timezone>` inside the `--schedule` value:

```
velero schedule create example-schedule --schedule="CRON_TZ=America/New_York 0 3 * * *"
velero schedule create example-schedule --schedule="CRON_TZ=Asia/Shanghai 0 3 * * *"
```

Names must come from the IANA Time Zone Database (the "TZ identifier" column, for example `America/New_York`).

Why use it: with a zone set, a schedule for 3am keeps running at 3am in that zone when daylight saving changes, which reduces disputes about when the backup ran.

Gotcha from the docs: jobs scheduled during daylight-savings leap-ahead transitions will not be run.

Cron field order is minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-6, Sunday to Saturday; 7 is also Sunday on some systems).

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Time zone specification" and the cron format block, read in full). Removed unsourced claims: the worked 2:30am example and advice, and the `spec.schedule` Schedule resource example.

Method: documentation only; no commands were run.
