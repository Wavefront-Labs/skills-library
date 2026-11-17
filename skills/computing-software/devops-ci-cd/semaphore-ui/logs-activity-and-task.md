---
id: computing-software.devops-ci-cd.semaphore-ui.logs-activity-and-task
name: logs-activity-and-task
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [logs, journalctl, activity-log, task-log, events-log, semaphore-ui]
level: practitioner
status: docs-checked
description: "Where Semaphore logs go: stdout for the server, database for task and activity logs, optional files in Pro."
sources:
  - https://semaphoreui.com/docs/admin-guide/logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server, task and activity logs

Goal: find the right log.

- Server log: Semaphore never writes log files by itself; everything goes to stdout.
  - systemd: `journalctl -u semaphore.service -f`
  - Docker: `docker logs -f my-semaphore-container`
- Task logs and the Activity log (user actions such as adding or removing templates, inventories, repositories and team members) are stored in the database, so they are covered by database backups.

Pro 2.10 and later can also write them to files:

```json
{
  "log": {
    "events": { "enabled": true, "logger": { "filename": "./events.log" } },
    "tasks": {
      "enabled": true,
      "logger": { "filename": "./tasks.log" },
      "result_logger": { "filename": "./task_results.log" }
    }
  }
}
```

Variables: `SEMAPHORE_EVENT_LOG_ENABLED`, `SEMAPHORE_EVENT_LOG_FORMAT` (empty for raw, or `json`), `SEMAPHORE_EVENT_LOGGER`, `SEMAPHORE_TASK_LOG_ENABLED`, `SEMAPHORE_TASK_LOG_FORMAT`, `SEMAPHORE_TASK_LOGGER`, `SEMAPHORE_TASK_RESULT_LOGGER`.

The `logger` object also takes `maxsize` (MB before rotation), `maxage` (days), `maxbackups`, `localtime` and `compress`. With an empty `filename` it falls back to a lumberjack file in the temporary directory.

Task history is kept in the database. By default every task is stored; set `max_tasks_per_template` (or `SEMAPHORE_MAX_TASKS_PER_TEMPLATE`) to keep only that many per template, and the oldest task logs are deleted when the limit is exceeded. Enterprise adds syslog forwarding of activity and task entries (`syslog` options `enabled`, `network`, `address`, `tag`; restart after changing them).

Verify: start a task and see it in the task history; with file logging on, see lines in `tasks.log`.

## Checked

2026-11-04: checked against the logs page. Removed two unconfirmed gotchas and added the documented logger options, task retention and Enterprise syslog forwarding.

Method: documentation only; no commands were run.
