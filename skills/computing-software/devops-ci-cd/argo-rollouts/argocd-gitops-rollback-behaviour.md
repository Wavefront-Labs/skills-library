---
id: computing-software.devops-ci-cd.argo-rollouts.argocd-gitops-rollback-behaviour
name: argocd-gitops-rollback-behaviour
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [argocd, gitops, rollback, degraded, faq, git, argo-rollouts]
level: advanced
status: docs-checked
description: "Understand that Argo Rollouts rollbacks never write to Git and how this interacts with Argo CD."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/FAQ/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Argo Rollouts does not depend on Argo CD or any other Argo project, and it knows nothing about Git. It only watches live Rollout objects.

When a rollout fails (for example analysis fails), Argo Rollouts switches traffic or scale back to the previous stable version and marks the Rollout Degraded. It does not change Git.

With Argo CD the sequence is:

1. Git is updated with version N+1; Argo CD syncs the Rollout.
2. Argo Rollouts applies N+1 with the chosen strategy.
3. N+1 fails; Argo Rollouts goes back to N in the cluster, no Git change.
4. The Rollout is Degraded in both tools, the cluster is healthy on N.
5. Argo CD takes no further action because the live object matches Git (both say N+1). There is no endless loop.

You are expected to fix the issue and roll forward with the next version. Argo CD rollbacks point the cluster back at a previous Git hash and are unrelated to Rollouts' own rollbacks, which switch the cluster back to the previous stable version. To make Argo Rollouts write back to Git you must orchestrate it with an external system or custom glue code, which is normally not needed.

Other FAQ answers:

- On first creation, a Rollout ignores strategy and creates a fully scaled ReplicaSet.
- The controller adds the `argo-rollouts.argoproj.io/managed-by-rollouts` annotation to Services and Ingresses it modifies.
- Blue-green keeps the old ReplicaSet for `scaleDownDelaySeconds`, tracked with the annotation `argo-rollouts.argoproj.io/scale-down-deadline`, so re-applying the old manifest within that time is a fast rollback.
- Multi-service dependent rollbacks need your own solution.
- Smoke tests: use Job or Web analysis.

Verify that the Rollout shows Degraded in the cluster while Git is unchanged.

## Checked

2026-11-08. Confirmed against the Argo Rollouts FAQ (read in full): no Git writes, rollback sequence with Argo CD, no endless loop, first deploy ignores strategy, managed-by-rollouts annotation, blue-green fast rollback annotation, dependent services and smoke test answers.

Removed or corrected: replaced the advice to revert in Git with the FAQ's roll-forward answer and Argo CD rollback explanation; removed the kubectl verify command.

Method: documentation only; no commands were run.
