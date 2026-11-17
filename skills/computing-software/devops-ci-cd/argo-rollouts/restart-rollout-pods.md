---
id: computing-software.devops-ci-cd.argo-rollouts.restart-rollout-pods
name: restart-rollout-pods
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [restart, restartat, rolling-recreate, pdb, maxunavailable, argocd-action, argo-rollouts]
level: practitioner
status: docs-checked
description: "Restart all pods of a Rollout without running the blue-green or canary process."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/restart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Restarting is useful for hygiene or to force startup logic again, such as reloading a modified Secret, when a full progressive update is undesirable.

```bash
kubectl argo rollouts restart ROLLOUT
```

If you use Argo CD with Rollouts there is a bundled restart action:

```bash
argocd app actions run my-app restart --kind Rollout --resource-name my-rollout
```

Both set `.spec.restartAt` to the current time as an RFC 3339 UTC string such as `2020-03-30T21:19:35Z`. That tells the controller every pod must have been created after this timestamp.

How it proceeds: the controller iterates each ReplicaSet, and every pod whose creation timestamp is older than `restartAt` is evicted so the ReplicaSet replaces it. To avoid disruption it deletes at most `maxUnavailable` pods at a time, and because pods are evicted rather than deleted, any PodDisruptionBudgets are honoured.

Order: the stable ReplicaSet first, then the current ReplicaSet, then all other ReplicaSets beginning with the oldest.

Consequences from the docs: a restart skips the regular blue-green or canary update strategy; restarting a single-replica Rollout causes downtime, because the pod must be terminated before it is replaced; it is slower than a Deployment rolling update because `maxSurge` is not used; if `maxUnavailable` is 0 the controller still restarts one pod at a time. Changing `spec.template` mid-restart cancels the restart and the normal update runs. Setting `.spec.restartAt` to a future time schedules a restart.

Verify with `kubectl get pods` showing new creation ages and `kubectl get rollout NAME -o jsonpath='{.spec.restartAt}'`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/restart/.

Removed or corrected: the strict-PDB slow-restart pitfall and the claim that no traffic-weight steps happen.

Method: documentation only; no commands were run.
