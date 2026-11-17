---
id: computing-software.cloud-infrastructure-engineering.kubernetes.replicationcontroller-migration
name: replicationcontroller-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, replicationcontroller, legacy-workloads, deployment-migration, orphan-cascade]
level: practitioner
status: docs-checked
description: "Migrate legacy ReplicationControllers to Deployments with no downtime by orphaning pods and letting a Deployment's ReplicaSet adopt or replace them under the same Service."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "https://kubernetes.io/docs/tasks/administer-cluster/use-cascading-deletion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating ReplicationControllers to Deployments

ReplicationController (`v1`) predates ReplicaSets: equality-only selectors and no declarative
rollouts (`kubectl rolling-update` was removed in Kubernetes 1.18). The docs say it is superseded
by the Deployment and ReplicaSet APIs, and that a Deployment configuring a ReplicaSet is the
recommended way to set up replication. A ReplicaSet is the next-generation RC with set-based
selectors; use a Deployment rather than a bare ReplicaSet unless you need custom update
orchestration.

## Find them
```bash
kubectl get rc -A
kubectl get rc web -o yaml > rc-web.yaml
```

## Zero-downtime migration
1. Write a Deployment with the **same pod template**, a selector that matches the existing
   pods' labels (convert `spec.selector` map to `selector.matchLabels`), same replicas.
   Add a new label to the template only if you also keep the old ones the Service selects.
2. Create the Deployment and wait for it to be fully available. Its ReplicaSet creates its
   own pods (the Deployment controller adds a `pod-template-hash` label to the ReplicaSet
   selector and pod template labels, which the RC's pods lack); you briefly run 2x
   replicas behind the Service, so check capacity and quota first.
3. Delete the RC **without** deleting pods, so nothing drops:
   ```bash
   kubectl delete rc web --cascade=orphan
   ```
4. Delete the orphaned old pods once the Deployment's pods are Ready (see gotcha below for
   the selector). Check the Service's endpoints throughout.

Simpler when brief overlap is unacceptable for capacity: scale the RC down step by step while
scaling the Deployment up.

## Gotchas
- Pod-template-hash: a Deployment's ReplicaSet selector includes `pod-template-hash`, so
  orphaned RC pods (no such label) do not match it. Plan to delete them after the Deployment is
  healthy, selecting them with the set-based `!key` form:
  `kubectl delete pod -l 'app=web,!pod-template-hash'`.
- If an HPA targets the `ReplicationController`, point its `scaleTargetRef` at the Deployment.
- GitOps: remove the RC manifest in the same change, or the tool recreates it.
- Within RCs themselves, a replacement RC with the same `.spec.selector` adopts the old pods,
  but does not make them match a different pod template; this is the RC-to-RC path, not RC to
  Deployment.

## Verify
- [ ] `kubectl get rc -A` empty; endpoints never dropped to zero during the change.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "ReplicationController", "Deployment" and
"Labels and Selectors" (latest release v1.37.1), and the Kubernetes 1.18 release notes
(`kubectl rolling-update` removal). Confirmed: RC superseded by Deployment/ReplicaSet,
`--cascade=orphan` deletes an RC without touching its pods, same-selector adoption between RCs,
`pod-template-hash` on the Deployment's ReplicaSet selector, set-based `!key` selectors.
Removed unconfirmed claims about tooling support and the endpointslice watch command.
Method: documentation only; no commands were run.
