---
id: computing-software.devops-ci-cd.deployment-strategies.ephemeral-environment-cost-control
name: ephemeral-environment-cost-control
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, scale-to-zero, ephemeral-environments, environments-management]
level: practitioner
status: draft
description: "Keep per-PR and preview environment costs down: TTL cleanup, scale-to-zero off hours (kube-green, KEDA HTTP), shared backing services and spot capacity."
sources: ["https://keda.sh/docs/latest/concepts/scaling-deployments/", "https://kube-green.dev/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ephemeral environment cost control (scale to zero)

Dozens of preview environments x full stacks x 24/7 = a bill bigger than production.

## Tactics
1. **TTL and cleanup**: delete on PR close/merge; sweeper job removes envs older than N days or
   with no commits for 72 h. Namespaces labelled with `pr`, `created-at`, `owner`.
2. **Sleep schedules**: kube-green `SleepInfo` scales Deployments to zero nights/weekends:
   ```yaml
   apiVersion: kube-green.com/v1alpha1
   kind: SleepInfo
   metadata: { name: off-hours, namespace: preview-pr-123 }
   spec:
     weekdays: "1-5"
     sleepAt: "20:00"
     wakeUpAt: "07:00"
     timeZone: "Europe/London"
   ```
3. **Scale to zero on idle**: KEDA HTTP add-on or Knative scale from zero on first request (cold
   start seconds); good for review apps opened occasionally.
4. **Share heavy dependencies**: one shared database server with a database per PR, shared
   Kafka with prefixed topics, instead of per-env clusters.
5. **Cheap capacity**: preview node pool on spot/preemptible instances with taints; smaller
   requests than production.
6. **Only what changed**: deploy the changed service; route other calls to shared staging services.

## Visibility
Cost per namespace (Kubecost/OpenCost) reported weekly; quota per preview namespace (ResourceQuota)
to cap runaway envs.

## Verify
- [ ] Preview spend per PR is known; no namespace older than the TTL exists; nights show near-zero preview pods.
