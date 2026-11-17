---
id: computing-software.collaboration-platform-administration.nextcloud.maintenance-window-start-setting
name: maintenance-window-start-setting
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [maintenance-window-start, config-php, background-jobs, occ, utc]
level: practitioner
status: docs-checked
description: "Set maintenance_window_start so non-time-sensitive daily Nextcloud jobs run only in a four-hour UTC window, and know it only applies in cron mode."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/background_jobs_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep heavy once-a-day jobs out of working hours.

Some background jobs run once a day. Those that advertise themselves as not time-sensitive, for example activity expiration, suspicious login training and update checks, are delayed during working hours and only run in the 4 hours after the configured hour.

Rules from the docs:
- The setting only takes effect in `cron` mode.
- The hour is in UTC, not server local time.
- A value of 1 means these jobs run between 01:00 and 05:00 UTC.
- A value of 100 means you do not care when they run. Resource-intensive jobs may then hit high-usage periods and slow users down.

In `config/config.php`:

```
'maintenance_window_start' => 1,
```

Or with `occ`, like any other system config value:

```
occ config:system:set maintenance_window_start --type=integer --value=1
```

Run `occ` as the web server user.

Choosing a value: convert your quietest local hours to UTC first. If your quiet period is 02:00 to 06:00 in UTC+10, the matching UTC start is 16 (previous day).

Check: confirm the scheduler is real cron (see background-jobs-scheduling-modes), then confirm `maintenance_window_start` in `config.php`.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/background_jobs_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
