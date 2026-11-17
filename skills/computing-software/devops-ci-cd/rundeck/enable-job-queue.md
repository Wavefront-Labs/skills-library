---
id: computing-software.devops-ci-cd.rundeck.enable-job-queue
name: enable-job-queue
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, job-queue, queue-size, poll-delay, multiple-executions]
level: practitioner
status: docs-checked
description: "Queue extra executions of a Rundeck job instead of rejecting them, set a queue size limit, tune polling delays, and disable the queue system (commercial)."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/job-queue.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a job runs one execution at a time and rejects further attempts unless Multiple Executions is enabled. Job Queue (commercial) instead accepts new executions and runs them sequentially in creation order. Each job has its own persistent queue that survives restarts. Scheduled runs are only queued when triggered while an execution is already running.

Enable: edit the job, find the `Job Queue` section, tick `Enable Job Queue`. Optionally set a queue size limit; at the limit further executions are rejected. Empty or 0 means unlimited.

Warnings:
- Enabling the queue overrides Multiple Executions.
- As of 3.4.0, jobs with secure options do not support queuing.

Use: just run the job; if one is running, the new one goes to the tail. Queued items show on the Activity page. Cancel one by killing it from its execution page.

`rundeck-config.properties`:

```properties
rundeck.jobQueue.enabled=false
rundeck.jobQueue.pollDelay=10
rundeck.jobQueue.startupDelay=10
```

- `enabled=false` removes all queue options; existing queued executions stay queued until killed, and per-job queue config is kept for when it is re-enabled.
- `pollDelay` (seconds, default 10): raise it on big clusters to ease database polling.
- `startupDelay` (seconds, default 10): wait after startup before processing.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Job Queue (Commercial): per-job persistent sequential queue, Enable Job Queue option and queue size limit (empty or 0 unlimited), overrides Multiple Executions, 3.4.0 secure-option limitation, scheduled runs queued only when triggered during a running execution, kill to cancel, and the rundeck.jobQueue.enabled, pollDelay and startupDelay properties with 10 second defaults. Nothing removed.

Method: documentation only; no commands were run.
