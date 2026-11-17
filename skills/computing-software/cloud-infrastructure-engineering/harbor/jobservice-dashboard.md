---
id: computing-software.cloud-infrastructure-engineering.harbor.jobservice-dashboard
name: jobservice-dashboard
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [jobservice, job-queues, worker-pool, pause-resume, harbor]
level: practitioner
status: docs-checked
description: "Inspect and control Harbor job queues, schedules and workers from the job service dashboard, including how to withdraw an execution."
sources:
  - https://goharbor.io/docs/main/administration/jobservice-dashboard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The dashboard is at `https://<harbor_url>/harbor/job-service-dashboard/` (Administration, Job Service Dashboard) and needs system administrator rights. The overview shows Pending Jobs In Queues (action **Stop All**), Schedules (**Pause All**, **Resume All**) and Workers as free/total (**Free All**).

**Job Queues** tab: Job Type, Pending Count, Latency, Paused. Per-queue actions: **Stop** removes all jobs from the queue and marks them Stopped; **Pause** and **Resume** only stop or start workers consuming the queue. They do not stop submission and do not change job status. Queue types: `GARBAGE_COLLECTION`, `IMAGE_SCAN`, `P2P_PREHEAT`, `PURGE_AUDIT`, `REPLICATION`, `RETENTION`, `SCAN_DATA_EXPORT`, `SCHEDULER`, `SLACK`, `SYSTEM_ARTIFACT_CLEANUP`, `WEBHOOK`. Pausing `SCHEDULER` prevents every periodical schedule from triggering.

**Schedules** tab: ID, Vendor Type, Vendor ID, Cron, Create Time.

**Workers** tab: pools (Worker Pool ID, PID, Start At, Heartbeat At, Concurrency); click a pool to list workers (Worker ID, Job Name, Job ID, Started At, Checked In At, Logs). **Free** stops the current job to free the worker and can take several minutes.

Withdrawing an execution: stopping one running task may not stop the whole execution. Click **Stop** on the queue in Job Queues, then **Free** on the workers, then wait for the execution status to become Stopped. To let workers handle other job types without discarding jobs, Pause the queue and Resume it later.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Job Service Dashboard.
Method: documentation only; no commands were run.
