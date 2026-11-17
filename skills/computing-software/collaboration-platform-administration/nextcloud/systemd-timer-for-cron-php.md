---
id: computing-software.collaboration-platform-administration.nextcloud.systemd-timer-for-cron-php
name: systemd-timer-for-cron-php
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [systemd, timer, cron-php, execcondition, killmode]
level: practitioner
status: docs-checked
description: "Replace the Nextcloud crontab entry with a systemd service and timer pair, using ExecCondition to skip runs when the instance is unhealthy."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/background_jobs_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run `cron.php` every 5 minutes from systemd rather than crontab.

Create two files in `/etc/systemd/system/`.

`nextcloudcron.service`:

```
[Unit]
Description=Nextcloud cron.php job

[Service]
User=www-data
ExecCondition=php -f /var/www/nextcloud/occ status -e
ExecStart=/usr/bin/php -f /var/www/nextcloud/cron.php
KillMode=process
```

`nextcloudcron.timer`:

```
[Unit]
Description=Run Nextcloud cron.php every 5 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min
Unit=nextcloudcron.service

[Install]
WantedBy=timers.target
```

Replace `www-data` with your HTTP server user and the paths with your install location.

Why the key lines matter:
- `ExecCondition` runs `occ status -e` first, and skips the job when the instance is not operating normally.
- `KillMode=process` is needed so external programs started by the cron job keep running after it finishes.
- `OnBootSec` starts the timer 5 minutes after boot, otherwise you must start it by hand; `OnUnitActiveSec` repeats it.
- The service unit needs no `[Install]` section. Earlier editions of the manual recommended one, so remove it from older setups.

Start and enable in one step:

```
systemctl enable --now nextcloudcron.timer
```

Check: the timer is active in systemd and the admin background-jobs setting shows Cron after the first run.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/background_jobs_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
