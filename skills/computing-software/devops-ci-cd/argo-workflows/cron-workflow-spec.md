---
id: computing-software.devops-ci-cd.argo-workflows.cron-workflow-spec
name: cron-workflow-spec
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [cron-workflow, schedules, concurrency-policy, starting-deadline-seconds, workflow-metadata]
level: practitioner
status: docs-checked
description: "Define a CronWorkflow with schedules, timezone, concurrencyPolicy, startingDeadlineSeconds, history limits and a when guard, and manage it with argo cron commands."
sources: ["https://argo-workflows.readthedocs.io/en/latest/cron-workflows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CronWorkflow spec and options
A CronWorkflow is a Workflow plus cron options. `spec.workflowSpec` has the same type as `Workflow.spec` and acts as the template for each run; generated Workflows get names derived from the CronWorkflow name (for example `test-cron-wf-tj6fe`). Use `spec.workflowMetadata` to add labels and annotations to them.

Key options:
- `schedules`: required, non-empty list of cron strings. Syntax matches Kubernetes CronJobs (robfig/cron).
- `timezone`: IANA name such as `America/Los_Angeles`; defaults to the machine timezone.
- `suspend`: `false` by default; true stops scheduling.
- `concurrencyPolicy`: `Allow` (default), `Replace` (remove old runs before starting the new one) or `Forbid`.
- `startingDeadlineSeconds`: default `0`; grace window after the last scheduled time in which a missed run is still started.
- `successfulJobsHistoryLimit` default `3`, `failedJobsHistoryLimit` default `1`.
- `when`: an expression evaluated at every schedule hit; the run happens only if it is true.

Crash recovery: if the controller is down over a scheduled minute, a `startingDeadlineSeconds` larger than the delay makes exactly one catch-up run happen, never several.

CLI: `argo cron create cron.yaml`, `argo cron list`, `argo cron get NAME`; `kubectl get cwf` also works. The displayed next run assumes the controller uses UTC. CronWorkflows can also be managed from the UI or by Argo CD.

## Checked
2026-11-03. Confirmed against the Argo Workflows Cron Workflows page: the options table with defaults, the schedule syntax note, crash recovery behaviour, the CLI commands, kubectl and the UTC note. Nothing removed.
Method: documentation only; no commands were run.
