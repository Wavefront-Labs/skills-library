---
id: computing-software.devops-ci-cd.argo-cd.health-status-semantics
name: health-status-semantics
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, health-status-progressing, health-suspended, health-degraded, app-health-aggregation]
level: practitioner
status: docs-checked
description: "Interpret Argo CD health states (Healthy, Progressing, Degraded, Suspended, Missing, Unknown), how app health aggregates, and how health gates waves, hooks and selfHeal."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/health/", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Health states and their semantics

States: Healthy, Progressing, Degraded, Suspended, Missing, Unknown. Per-kind rules are on the health page, for example: an Ingress is healthy only when `status.loadBalancer.ingress` has at least one hostname or IP; a CronJob whose last job failed is Degraded and one whose last job is running is Progressing; a Job with `.spec.suspended` true is Suspended; a PersistentVolumeClaim needs `status.phase` Bound.

## Aggregation
Application health is the worst health of its immediate child resources, by priority from most to least healthy: Healthy, Suspended, Progressing, Missing, Degraded, Unknown.

## Where health matters
- **Sync waves**: the next wave is applied only when earlier waves are in sync and healthy, so a resource that cannot become healthy in an early wave can stop the app ever becoming healthy.
- Alert on Degraded; treat Suspended at an expected pause as normal.

## Verify
- [ ] The CD pipeline waits for the application to be Healthy and fails on Degraded within its timeout.

## Checked
2026-10-28. Confirmed on the Argo CD health page: the six states, the aggregation rule (worst immediate-child health, priority Healthy, Suspended, Progressing, Missing, Degraded, Unknown), and the Ingress, CronJob, Job and PersistentVolumeClaim rules quoted. Confirmed on the sync waves page: later waves wait for earlier waves to be in sync and healthy, and an unhealthy resource in an early wave can stop the app reaching healthy.
Removed (not confirmed): the "typical cause" table, the `argocd app wait --health --sync --timeout` command, the `on-health-degraded` trigger, `--show-operation` and `argocd app resources` debugging commands, and Rollouts behaviour.

Method: documentation only; no commands were run.
