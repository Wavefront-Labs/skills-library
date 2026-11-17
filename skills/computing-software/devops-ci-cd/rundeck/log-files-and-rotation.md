---
id: computing-software.devops-ci-cd.rundeck.log-files-and-rotation
name: log-files-and-rotation
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, service-log, logrotate, log-files, copytruncate]
level: practitioner
status: docs-checked
description: "Find Rundeck server log files by install type and rotate service.log on Linux with logrotate, plus the Windows caveat that the file is locked while running."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/maintenance/logs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Log directory: RPM `/var/log/rundeck`, launcher `$RDECK_BASE/server/logs`.

Files:
- `command.log`: shell tool activity
- `rundeck.audit.log`: authorization messages for aclpolicy
- `rundeck.audit.events.log`: all auditing events
- `rundeck.jobs.log`: job definition changes (the page also writes `rundeck.job.log`)
- `rundeck.options.log`: remote HTTP requests for option JSON data
- `rundeck.log`: general application messages
- `service.log`: standard input and output at runtime

Customise formats and locations in the log4j properties section of the config reference.

Rotate `service.log` on Linux (needs `logrotate`). Create `/etc/logrotate.d/theRundeckLog`:

```
/var/log/rundeck/service.log {
 su root root
 copytruncate
 daily
 missingok
 rotate 7
 compress
 delaycompress
 notifempty
 create 640 root adm
}
```

Schedule it, for example monthly: `echo "@monthly root logrotate /etc/logrotate.d/theRundeckLog" >> /etc/crontab`.

Test: `logrotate --debug --force /etc/logrotate.d/theRundeckLog`. Backups should appear beside service.log.

Windows: the page offers a PowerShell script or LogRotateWin. Windows locks `service.log` while Rundeck uses it, so rotate when the service is stopped (the script runs before start and after stop).

## Checked

2026-11-04. Confirmed against the Rundeck docs page Logs: RPM and launcher log directories, the seven log files and their purposes (the page lists rundeck.jobs.log in the tree and rundeck.job.log in the description), logrotate config, cron line, logrotate --debug --force test, and the Windows PowerShell script and LogRotateWin methods with the note that Windows locks service.log while in use. Nothing removed.

Method: documentation only; no commands were run.
