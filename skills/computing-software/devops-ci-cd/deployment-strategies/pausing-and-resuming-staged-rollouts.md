---
id: computing-software.devops-ci-cd.deployment-strategies.pausing-and-resuming-staged-rollouts
name: pausing-and-resuming-staged-rollouts
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, rollout-pause-resume, staged-rollout, argo-rollouts-pause, kubectl-rollout-pause, halt-rollout, app-store-phased-release]
level: practitioner
status: draft
description: "Pause and resume staged rollouts safely: Kubernetes rollout pause, Argo Rollouts pause steps and abort, CodeDeploy stop, CodeDeploy stop and mobile phased releases."
sources:
  - https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#pausing-and-resuming-a-deployment
  - https://argoproj.github.io/argo-rollouts/features/specification/
  - https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases
  - https://support.google.com/googleplay/android-developer/answer/6346149
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pausing and resuming staged rollouts

Pausing freezes the current mix of old and new versions while you investigate. It is not a rollback: users already on the new version stay there.

## Kubernetes Deployment
```bash
kubectl rollout pause deploy/web          # stops further ReplicaSet scaling; current pods stay
kubectl rollout status deploy/web         # shows "paused"
kubectl set image deploy/web web=img:fix  # changes accumulate while paused (no rollout starts)
kubectl rollout resume deploy/web
kubectl rollout undo deploy/web           # actual rollback
```
`progressDeadlineSeconds` doesn't count time spent paused.

## Argo Rollouts
```yaml
strategy:
  canary:
    steps:
    - setWeight: 10
    - pause: { duration: 15m }   # timed pause
    - setWeight: 50
    - pause: {}                  # indefinite: needs manual promote
```
```bash
kubectl argo rollouts get rollout web --watch
kubectl argo rollouts pause web        # pause at the current step
kubectl argo rollouts promote web      # continue past a pause (or --full to skip all steps)
kubectl argo rollouts abort web        # back to stable weights, rollout marked Degraded
kubectl argo rollouts retry rollout web
```
Failed analysis aborts automatically; inconclusive analysis pauses for a human.

## AWS CodeDeploy / ECS
```bash
aws deploy stop-deployment --deployment-id d-ABC --auto-rollback-enabled   # stop and roll back
```
CodeDeploy has no true pause; use a longer bake (`TerminationWaitTime`, linear configs) or lifecycle hooks that wait for approval.

## Mobile app stores
- Apple phased release (7 days, 1-2-5-10-20-50-100%): pause in App Store Connect for up to 30 days total; users can still update manually from the store.
- Google Play staged rollout: halt rollout in Play Console (`Halt rollout`), resume or release a fixed version with a higher version code. Users who already updated keep the bad version: fix forward.

## Feature flag progressive rollouts
Pausing = stop increasing the percentage; scheduled rollouts in flag tools (LaunchDarkly, Unleash) can be paused per flag. Kill switch for real rollback.

## Operating rules
- Pause on ambiguous signals; abort/rollback on clear ones. Don't leave rollouts paused for days: mixed versions complicate debugging and later deploys.
- Announce the pause (deploy channel) and who owns the decision to resume.
- Pipelines must detect the paused state and not start another deploy on top.

## Verify
- [ ] Pausing halts weight/replica changes (observe for 10 minutes); resume continues from the same step.
- [ ] Abort returns traffic to stable and the team knows the command for each platform used.
