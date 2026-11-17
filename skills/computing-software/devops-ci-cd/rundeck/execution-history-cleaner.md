---
id: computing-software.devops-ci-cd.rundeck.execution-history-cleaner
name: execution-history-cleaner
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, execution-history-cleaner, retention-days, history-cleanup, project-properties]
level: practitioner
status: docs-checked
description: "Enable the per-project Execution History Cleaner in Rundeck with retention days, minimum to keep, batch size and a Quartz cron schedule."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/projects/execution-history-cleaner.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page calls the cleaner the recommended way to purge Activity history; it is far cheaper than deleting executions one by one through the API. It deletes execution records and reports, referenced data, file upload records, local, partial and state files, and remote log files if log storage is configured. It never deletes running executions.

Configure in Project Settings, Edit Configuration, or `project.properties`:

```properties
project.execution.history.cleanup.enabled=true
project.execution.history.cleanup.retention.days=60
project.execution.history.cleanup.retention.minimum=50
project.execution.history.cleanup.batch=500
project.execution.history.cleanup.schedule=0 0 2 * * ?
```

- `enabled`: default disabled.
- `retention.days`: default 60; completed executions older than this are candidates.
- `retention.minimum`: default 50; deletions are reduced so at least this many remain, oldest deleted first. If the total is below the minimum, nothing is deleted.
- `batch`: default 500 deletions per run; the rest go in later runs.
- `schedule`: Quartz cron, default `0 0 0 1/1 * ? *` (daily at midnight). In a cluster only one server runs it per project.

Advice: start conservative and watch the first runs. For a big backlog, temporarily raise batch size (1000-2000) and run more often, then restore.

Verify in the server logs: look for lines such as `Max days to keep: 60` and `Deleted 45 of 45 executions`.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Execution History Cleaner: recommended approach, what is deleted, the five project.execution.history.cleanup.* properties with defaults (disabled, 60 days, 50 minimum, batch 500, Quartz cron 0 0 0 1/1 * ? *), minimum and batch semantics, cluster behaviour, backlog advice and the log lines. Nothing removed.

Method: documentation only; no commands were run.
