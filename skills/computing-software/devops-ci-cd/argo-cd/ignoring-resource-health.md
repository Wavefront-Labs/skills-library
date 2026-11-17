---
id: computing-software.devops-ci-cd.argo-cd.ignoring-resource-health
name: ignoring-resource-health
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, job-health-ignore, ignore-healthcheck, health-override, non-critical-resources]
level: practitioner
status: docs-checked
description: "Exclude non-critical resources from Argo CD application health with the ignore-healthcheck annotation, or override health checks for kinds that misreport."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/health/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ignoring resource health

## 1. Per resource
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: nightly-report-seed
  annotations:
    argocd.argoproj.io/ignore-healthcheck: "true"
```
The resource's health no longer affects the health of its parent Application. Use for:
- Jobs whose failure should not mark the service Degraded (optional seeders, smoke checks you alert on separately);
- LoadBalancer Services/Ingresses in environments with no LB controller (kind/dev clusters);
- CRs whose operator is known to misreport.

## 2. Per kind (all apps): override with a trivial check
```yaml
# argocd-cm
data:
  resource.customizations.health.batch_Job: |
    hs = { status = "Healthy", message = "health ignored for Jobs" }
    return hs
```
Too broad for most clusters — prefer the annotation.

## 3. Hooks
Hooks use `argocd.argoproj.io/hook` and `argocd.argoproj.io/hook-delete-policy` (for example `HookSucceeded`) to control when a hook resource is deleted; see the resource hooks docs.

## Gotchas
- Ignoring health of something waves depend on removes the wait — the next wave starts immediately.
- Do not use it to hide a genuinely broken Deployment; fix the probe or rollout instead.

## Verify
- [ ] With the annotated Job failed, the Application health is not affected by it.

## Checked
2026-10-28. Confirmed on the Argo CD health page: the `argocd.argoproj.io/ignore-healthcheck: "true"` annotation, whose effect is that the resource's health does not affect its parent Application; key format `resource.customizations.health.<group_kind>` with `hs.status` and `hs.message`; `argocd.argoproj.io/hook-delete-policy` with `HookSucceeded` exists. Confirmed on the sync waves page: later waves wait for earlier waves to be healthy.
Removed (not confirmed): the claim that the resource still shows its own health in the UI, and the statement that a failed hook fails the sync.

Method: documentation only; no commands were run.
