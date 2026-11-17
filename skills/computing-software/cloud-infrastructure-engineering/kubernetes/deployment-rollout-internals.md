---
id: computing-software.cloud-infrastructure-engineering.kubernetes.deployment-rollout-internals
name: deployment-rollout-internals
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, deployment, rollout, revisionhistorylimit, progressdeadlineseconds, proportional-scaling, rollout-pause, rollout-resume, rollout-restart, kubectl-rollout, maxsurge, maxunavailable, stuck-rollout, deployment-condition, replicaset-revision, minreadyseconds, rollout-status]
level: advanced
status: docs-checked
description: "How a Deployment rollout actually proceeds: two ReplicaSets converging, rollover, proportional scaling, revision history, pause/resume, progressDeadlineSeconds, stuck rollouts."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/", "https://github.com/kubernetes/kubernetes/blob/release-1.37/staging/src/k8s.io/kubectl/pkg/polymorphichelpers/objectrestarter.go", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_status/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Deployment rollout internals — what happens between `kubectl apply` and "done"

**Goal:** diagnose a rollout that's slow, stuck, or scaling oddly by knowing the actual
algorithm, not just the surface commands. Basic `maxSurge`/`maxUnavailable` and PDB usage
are in `computing-software.cloud-infrastructure-engineering.kubernetes.deployments-services-and-probes`;
this is the mechanics underneath them.

## 1. A rollout is ReplicaSets converging, not an in-place pod update
Changing `spec.template` never mutates pods. The Deployment controller:
1. Finds or creates a ReplicaSet for the new pod template; the `pod-template-hash` label on the
   ReplicaSet and its pods identifies the template.
2. Scales the **new** RS up and the **old** RS down, bounded by `maxSurge`/`maxUnavailable`
   converted from percentage to an absolute count (surge rounds up, unavailable rounds down;
   both default to 25%).
3. Repeats until the new RS = desired replicas and old ReplicaSets = 0, then keeps old
   ReplicaSets scaled to 0 up to `revisionHistoryLimit`.
- **Rollover**: if you update the template while a rollout is in progress, the controller
  creates another ReplicaSet and moves the one it was scaling up onto its list of old
  ReplicaSets, scaling it down immediately rather than finishing the first rollout. This is
  why rapid successive edits can leave more than two non-zero ReplicaSets briefly.
- **Proportional scaling**: if you (or an autoscaler) change `replicas` while a rollout is in
  progress or paused, the controller spreads the added or removed replicas across the active
  ReplicaSets in proportion to their size, rather than putting them all in the newest one.

## 2. Revision history and rollback
Each ReplicaSet carries the rollout's revision in the `deployment.kubernetes.io/revision`
annotation (`kubectl rollout history deploy/api --revision=N` prints the pod template).
Rollback (`kubectl rollout undo`) does **not** replay history forward: it reuses the stored
template from the target revision's ReplicaSet and runs the normal rollout.
- `revisionHistoryLimit` (default 10) caps how many old ReplicaSets are kept. Once an old
  ReplicaSet is deleted, you can no longer roll back to that revision; 0 removes all history.
  Cleanup only starts after the Deployment reaches a complete state, so a Deployment that
  never completes can hold more ReplicaSets than the limit.
- `spec.selector` is immutable in apps/v1; changing it means deleting and recreating the
  Deployment.

## 3. Pause, resume, and restart
- `kubectl rollout pause deploy/api`: template changes made while paused do not trigger new
  rollouts until `kubectl rollout resume`, so several edits roll out together. Progress is
  not checked against the deadline while paused, and a paused Deployment cannot be rolled
  back until resumed. Useful for canary-by-hand.
- `kubectl rollout restart deploy/api` sets a `kubectl.kubernetes.io/restartedAt` timestamp
  annotation on `spec.template.metadata.annotations`, so the template changes and a normal
  rollout replaces the pods (for example to pick up a changed ConfigMap) without a raw pod
  delete.

## 4. progressDeadlineSeconds and stuck rollouts
`spec.progressDeadlineSeconds` (default 600) is how long the controller waits for progress
before setting the `Progressing` condition to `False` with reason `ProgressDeadlineExceeded`.
Kubernetes takes no other action: there is **no automatic rollback**, and the controller keeps
retrying. A human, pipeline or higher-level orchestrator still has to run `rollout undo`.
Causes of a stuck rollout:
- New pods `Pending` (quota, taints, PVC zone) or `CrashLoopBackOff`/failing readiness:
  the new RS never reaches its target, so the old RS never scales to 0.
- `minReadySeconds` (default 0) delays a Ready pod counting as available. The deadline must be
  greater than `minReadySeconds`; a deadline only slightly larger can time out a rollout that
  is healthy but slow.
- PodDisruptionBudgets do **not** block a Deployment rollout: workload controllers are not
  limited by PDBs during rolling updates (pods replaced still count against the budget for
  other evictions such as drains). Rollout safety comes from `maxUnavailable` and readiness.

## Gotchas
- `kubectl rollout status` waits for the rollout and returns a non-zero exit code once the
  progress deadline is exceeded; add `--timeout` in CI so the job cannot hang.
- Editing the Deployment directly in a GitOps-managed cluster while a controller is also
  reconciling it causes a fight; pause the GitOps sync, not just the rollout.
- A rollback via `rollout undo` is itself a new revision (rolling back to revision 2 from 3
  produces revision 4), so a second plain `undo` returns to the revision you just left; use
  `--to-revision` to name the target.

## Verify
- [ ] `kubectl rollout history deploy/api` shows the expected number of revisions and each
      `--revision=N` prints the template you expect.
- [ ] A deliberately bad image rollout shows `Progressing=False, ProgressDeadlineExceeded`
      in `kubectl describe deploy/api` conditions after `progressDeadlineSeconds`.
- [ ] `kubectl rollout restart` on a Deployment with an unchanged image still produces new
      pod names/start times.
- [ ] `kubectl get rs -l app=api` shows one non-zero ReplicaSet once a rollout settles.

## Checked
Checked 2026-10-27 against kubernetes/website (main tree, v1.38 development; latest release
v1.37): Deployments (rollover, proportional scaling applies when replicas change mid-rollout,
maxSurge rounds up and maxUnavailable rounds down with 25% defaults, revisionHistoryLimit
default 10 and cleanup after completion, progressDeadlineSeconds default 600 with no action
beyond the condition, minReadySeconds default 0, pause behaviour, undo creating a new revision,
`rollout status` exit codes), Disruptions (workload resources are not limited by PDBs during
rolling upgrades) and the kubectl objectrestarter source in kubernetes/kubernetes release-1.37
(`kubectl.kubernetes.io/restartedAt`). Corrected the claims that proportional scaling describes
successive template edits and that a PDB can block a Deployment rollout; replaced prose
`sources:` titles with URLs.

Method: documentation only; no commands were run.
