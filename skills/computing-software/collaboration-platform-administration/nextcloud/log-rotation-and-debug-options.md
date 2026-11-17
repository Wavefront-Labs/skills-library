---
id: computing-software.collaboration-platform-administration.nextcloud.log-rotation-and-debug-options
name: log-rotation-and-debug-options
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [log-rotate-size, log-backtrace, log-query, loglevel-frontend, logging]
level: advanced
status: docs-checked
description: "Tune Nextcloud log rotation with log_rotate_size, and use log.backtrace, log_query and loglevel_frontend only for debugging because of their volume."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/logging_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound log growth and know which switches are debug-only.

All settings live in `config/config.php` and apply to file-based logging.

`log_rotate_size`: enables rotation and limits log size, in bytes. When the current file reaches the size a new file is created. If a rotated file already exists, it is overwritten. Set `0` to disable rotation. Default is `104857600` (100 MB):

```
"log_rotate_size" => 100 * 1024 * 1024,
```

Because an old rotated file is overwritten, ship logs elsewhere if you need history beyond one rotation.

`log.backtrace`: appends a backtrace to every log line, not only exceptions. Significantly increases log size; debugging only. Default `false`.

`log_query`: appends all database queries and their parameters to the log. Produces very large files; debugging only. Default `false`.

`loglevel_frontend`: separate level for messages from the browser frontend. Accepts 0 to 4 like `loglevel`. Default `2` (WARN).

Related defaults: `logfilemode` is `0640` and `logtimezone` is `UTC`.

A safe debugging routine:
1. Set `loglevel` to 0 and enable the one extra option you need.
2. Reproduce the problem.
3. Revert every option, since leaving them on grows logs quickly.

Check: after reverting, new log lines no longer carry backtraces or query text, and file size stops climbing quickly.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/logging_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
