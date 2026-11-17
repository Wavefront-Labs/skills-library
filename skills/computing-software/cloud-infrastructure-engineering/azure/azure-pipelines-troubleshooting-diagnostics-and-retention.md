---
id: computing-software.cloud-infrastructure-engineering.azure.azure-pipelines-troubleshooting-diagnostics-and-retention
name: azure-pipelines-troubleshooting-diagnostics-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-pipelines, pipeline-troubleshooting, pipeline-diagnostics, pipeline-retention, system-debug, agent-diagnostics, queued-runs, retention-leases, flaky-pipelines, yaml-validation]
level: practitioner
status: docs-checked
description: "Troubleshoot Azure Pipelines: runs that don't trigger or stay queued, system.debug and agent diagnostics, YAML expansion, auth failures, and retention policies and leases."
sources: ["https://learn.microsoft.com/en-us/azure/devops/pipelines/troubleshooting/troubleshooting", "https://learn.microsoft.com/en-us/azure/devops/pipelines/troubleshooting/review-logs", "https://learn.microsoft.com/en-us/azure/devops/pipelines/policies/retention"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Pipelines troubleshooting, diagnostics and retention

**Goal:** a fast route from "the pipeline failed / didn't run / is stuck" to the cause, and
retention settings that keep what auditors need without filling storage.

## 1. Didn't trigger
- YAML `trigger`/`pr` in the branch **being pushed** governs CI; a UI override (*Triggers → Override YAML*) silently wins — check it.
- Path filters, `batch: true`, skip-CI text in the commit message, draft PRs (`pr: drafts: false`).
- PR triggers for Azure Repos come from **build validation branch policies**, not the `pr:` key.
- GitHub: app/OAuth connection lost or webhook failing (GitHub → repo settings → webhooks deliveries).
- Pipeline disabled or *paused* in settings; scheduled triggers only run when the branch changed unless set to run always.

## 2. Stuck in queue
- *Waiting for an available agent*: parallel job limit reached (Org settings → Parallel jobs), pool
  empty, agents offline, or **demands** no agent satisfies. View: run → *View agent selection*.
- *Waiting for approval/check* or *needs permission* to a resource (first use of a service connection,
  environment, repo, variable group) — authorise in the run banner.
- Self-hosted: check the agent's `_diag` logs; capacity in VMSS/Managed DevOps Pools.

## 3. Failed — get more evidence
```yaml
variables:
  system.debug: true        # verbose task logs (or tick *Enable system diagnostics* when queuing)
  agent.diagnostic: true    # extra logs for self-hosted agent network issues; set automatically when system.debug is true (agent v2.200.0+)
```
- Download all logs: run results → ⋯ → *Download logs*.
- Validate expanded YAML (templates and expressions resolved) before pushing: test with `az pipelines run --name app-ci --branch feature/x` on a test branch.
- Common fixes: authorization errors → service connection lacks RBAC or federated credential subject mismatch;
  a service connection unused for 100 days can be disabled by Azure Pipelines — re-enable it;
  `Resource not authorized` → authorise the resource for this pipeline; task version missing → pin `@N` majors; intermittent npm/nuget failures → caching + retry.

## 4. Retention
- Project settings → *Pipelines → Settings → Retention*: days to keep artifacts/symbols/attachments,
  runs, and pull request runs; a minimum number of runs can be kept regardless of the days setting.
- **Retention leases** extend the lifetime of specific runs (e.g. every production deployment) beyond the configured period. Add or delete them with the Lease API, from a script in the pipeline using the predefined `runId` and `definitionId` variables, or manually.
- Disk on self-hosted agents: `workspace: clean: all` or agent maintenance jobs (pool settings).

## Gotchas
- `system.debug` may print sensitive non-secret values; secrets stay masked, but turn it off afterwards.
- Variables set via `##vso[task.setvariable]` are available only in **subsequent** steps (and other jobs only if `isOutput=true` and referenced via `dependencies`).
- Condition `succeeded()` is implicit; adding a custom condition without it runs the step after failures.

## Verify
- [ ] For a reproduced failure, the expanded YAML and debug logs identify the step and cause.
- [ ] Retention policy documented; production runs carry retention leases.
- [ ] Queue time and failure rate per pipeline reviewed (Pipelines → Analytics) with flaky tasks ticketed.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: system.debug, Agent.Diagnostic (set automatically with system.debug, agent v2.200.0+), Download logs, retention settings, retention leases via the Lease API, service connection disabled after 100 days of inactivity.

Removed because not confirmed: the lease request body, TF401019, retryCountOnTaskFailure, skip-CI strings, schedule always flag, previewRun, and the pipeline-deletion claim; the dead pipeline-run-not-starting source was dropped.

Method: documentation only; no commands were run.
