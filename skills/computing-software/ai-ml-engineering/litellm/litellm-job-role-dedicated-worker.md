---
id: computing-software.ai-ml-engineering.litellm.litellm-job-role-dedicated-worker
name: litellm-job-role-dedicated-worker
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, litellm-job-role, background-jobs, scheduled-job-stagger]
level: sme
status: docs-checked
description: "Run LiteLLM background jobs on a dedicated worker with LITELLM_JOB_ROLE and stagger scheduled jobs."
sources:
  - https://docs.litellm.ai/docs/proxy/prod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The proxy registers a scheduler of background jobs once per Uvicorn worker process, not once per pod, so a pod started with `--num_workers 4` runs four copies of every job. Jobs with a shared effect (resetting budgets, pruning spend logs, usage export) elect a single owner through Redis; without Redis there is nothing to elect through.

`LITELLM_JOB_ROLE`:

- unset or `all`: every job (default).
- `worker`: every job, including the single-owner ones.
- `serving`: no single-owner job.

Parsing is case insensitive; an unrecognised value falls back to `all` and logs a warning.

A `serving` pod stops registering the budget reset, spend log cleanup, key rotation, expired Admin UI session key cleanup and the weekly and monthly spend reports. It still registers the spend flush, daily tag spend flush, gateway request counter flush, config reload and database model and credential reloads, because each drains that pod's own state.

Topology: a Deployment of N replicas with `LITELLM_JOB_ROLE=serving`, plus one replica with `worker`, both using the same image, database and Redis. Point the Service and Ingress at the serving Deployment only.

Verify: the elected pod logs `<job name>: pod <id> owns this run` at INFO, and the Prometheus gauge `litellm_pod_lock_manager_size` carries a `<job>:<pod>` label.

Staggering: jobs are offset by default to avoid thundering herds. For a large cluster widen the window:

```
general_settings:
  scheduled_job_stagger:
    window_seconds: 600
    offsets:
      update_spend_job: 0
```

Offsets never touch cron schedules you supplied. Replica identity uses `POD_NAME`, then `HOSTNAME`, plus the worker process id.

## Checked

2026-11-03. Confirmed on the LiteLLM production page (docs.litellm.ai/docs/proxy/prod): per-worker job registration, LITELLM_JOB_ROLE values and case-insensitive parsing, which jobs a serving pod skips and keeps, the serving plus one worker topology, the owns this run log and litellm_pod_lock_manager_size, scheduled_job_stagger and POD_NAME / HOSTNAME identity.

Method: documentation only; no commands were run.
