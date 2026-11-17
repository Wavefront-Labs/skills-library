---
id: computing-software.collaboration-platform-administration.nextcloud.log-levels-and-log-type
name: log-levels-and-log-type
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [logging, loglevel, log-type, errorlog, nextcloud-log]
level: practitioner
status: docs-checked
description: "Set Nextcloud loglevel 0 to 4, choose log_type errorlog or file, and control log location, date format and the in-app log viewer."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/logging_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: log enough to diagnose without filling the disk.

Levels (set `loglevel` in `config/config.php`):
- 0 DEBUG: all activity, most detailed
- 1 INFO: user logins and file activity, plus everything below
- 2 WARN: operations succeed with warnings of potential problems (the default)
- 3 ERROR: an operation fails but other services continue
- 4 FATAL: the server stops

Use DEBUG to diagnose a problem, then reset it to a less verbose level.

Types (`log_type`):
- `errorlog`: sends everything to PHP `error_log()`, with entries prefixed `[nextcloud]`.
- `file`: writes a separate log, `nextcloud.log` by default, in the directory set by `datadirectory`. This is the type the admin page log viewer (*Administration settings -> Logging*) can read.

File example:

```
"log_type" => "file",
"logfile" => "nextcloud.log",
"loglevel" => 3,
"logdateformat" => "F d, Y H:i:s",
```

`logdateformat` uses PHP date codes. The default is `c`, which gives `2013-01-10T15:20:25+02:00`; the example above gives `January 10, 2013 15:20:25`.

Optional file parameters: `logfilemode` (defaults to `0640`), `logtimezone` (defaults to `UTC`), and the rotation, backtrace and query options covered in log-rotation-and-debug-options.

The separate optional `admin_audit` app has its own log.

Check: change `loglevel`, trigger a known warning, and confirm it appears in the file or the viewer.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/logging_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
