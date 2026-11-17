---
id: computing-software.devops-ci-cd.spinnaker.orca-zombie-executions
name: orca-zombie-executions
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [orca, zombie-executions, troubleshooting, queue, redis, admin-api, metrics]
level: sme
status: docs-checked
description: "Diagnose zombie Orca executions that show RUNNING with no queued work: log silence test, queue.zombieCheck.enabled, queue.zombies alert, queue rehydration and forced cancel."
sources:
  - https://spinnaker.io/docs/guides/runbooks/orca-zombie-executions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A **zombie** (or orphaned) execution has status RUNNING in the database but no messages in Orca's work queue or unacked set, so nothing is happening.

**Diagnosis.** Orca's `QueueProcessor` regularly logs `Received message RunTask(...)` lines for running executions. If nothing has been logged for a RUNNING execution for over 10 minutes, it is very likely a zombie.

**Detection and alerting.** Set `queue.zombieCheck.enabled: true` in Orca configuration. The check is expensive with `RedisExecutionRepository` and off by default. Zombies are then logged (`Found zombie executionType=pipeline application=...`) and emitted as the metric `queue.zombies`; alert when it is greater than 0.

**Remediation.** First try to rehydrate the queue, reissuing messages from the last stored state, with an Orca admin API that must be called on Orca directly (not exposed through Gate). It takes one execution or a time range and dry-runs by default; pass `dryRun=false` to apply:

```
POST /admin/queue/hydrate?executionId=<id>&dryRun=false
```

The response lists per-execution actions (for example "Task is running and is retryable") and a final `canApply`; if any part of an execution cannot be rehydrated the whole execution is skipped. It is best effort, especially if the execution zombied during a non-retryable task. If rehydration fails, cancel the execution from the UI or force it:

```
PUT /admin/forceCancelExecution?executionId=<id>&executionType=PIPELINE
```

**Causes.** Loss of the Redis behind Orca's queue, or prolonged unreliable networks. With `RedisExecutionRepository`, losing the Redis likely loses running executions too. With the SQL backend you lose only in-flight queue state; after Redis returns it has no messages, so existing RUNNING executions sit unprocessed until killed.

## Checked

2026-11-04. Definition, the 10-minute log heuristic, config key, metric, the hydrate and forceCancelExecution endpoints and the known causes were confirmed on the Orca Zombie Executions page. Removed: the `/admin/queue/zombies` kill endpoints and `minimumActivity` advice (not on the page).

Method: documentation only; no commands were run.
