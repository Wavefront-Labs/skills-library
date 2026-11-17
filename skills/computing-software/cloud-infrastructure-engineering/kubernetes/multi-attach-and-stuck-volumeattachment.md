---
id: computing-software.cloud-infrastructure-engineering.kubernetes.multi-attach-and-stuck-volumeattachment
name: multi-attach-and-stuck-volumeattachment
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-attach, volumeattachment, readwriteonce, readwriteoncepod, node-failure, force-delete, attach-detach-controller, stuck-pod, forcedetach]
level: advanced
status: docs-checked
description: "Diagnosing and safely resolving Multi-Attach errors and stuck VolumeAttachment objects when a ReadWriteOnce volume won't follow a pod to its new node."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes", "https://kubernetes.io/docs/concepts/cluster-administration/node-shutdown/#non-graceful-node-shutdown", "https://github.com/kubernetes/kubernetes/blob/master/pkg/controller/volume/attachdetach/reconciler/reconciler.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-Attach errors and stuck VolumeAttachments

**Goal:** when a Pod cannot start because its volume is attached elsewhere, know when waiting, the documented out-of-service taint, or manual action is appropriate.

## 1. The error
The attach/detach controller reports an event like `Multi-Attach error for volume "pvc-..." Volume is already used by pod(s) <name>` (or "in different namespaces") when a volume that does not allow multi-attach is still attached to another node. `ReadWriteOnce` means one node, not one Pod: several Pods on the same node can use it; `ReadWriteOncePod` (stable in 1.29, CSI volumes only) restricts the volume to a single Pod across the cluster.

## 2. The normal case
If the old Pod is terminating on a healthy node, wait for the detach to finish.
```bash
kubectl get pod <old-pod> -o wide
kubectl get volumeattachment
```

## 3. The node is gone
If a node shuts down without the kubelet's shutdown manager noticing, StatefulSet Pods stay in Terminating, VolumeAttachments are not deleted and the volume cannot attach elsewhere. The documented remedy (non-graceful node shutdown, stable in 1.28) is to add the taint `node.kubernetes.io/out-of-service` with effect `NoExecute` or `NoSchedule` to the node:
```bash
kubectl taint nodes <node-name> node.kubernetes.io/out-of-service=nodeshutdown:NoExecute
```
Pods without a matching toleration are force deleted and volume detach happens immediately. Before tainting, verify the node is shut down or powered off (not restarting), and remove the taint yourself after the Pods have moved and the node has recovered.

Separately, if a Pod deletion has not succeeded for 6 minutes, Kubernetes force detaches volumes when the node is unhealthy at that instant. Any workload still running on the node that uses a force-detached volume violates the CSI specification, which is why confirming the node is really down matters.

## 4. Do not shortcut
Deleting a VolumeAttachment or force-deleting a Pod only changes Kubernetes bookkeeping; it does not prove the old node stopped writing. Check the infrastructure view of the instance, and use the provider's own detach procedure (see your provider's current documentation) only when the instance is confirmed gone.

## Gotchas
- Abrupt node removal (autoscaler scale-in, spot reclaim) is a common trigger; drain nodes so Pods terminate cleanly.
- `ReadWriteOncePod` does not change the node-failure recovery story.

## Verify
- [ ] Distinguished "old Pod still terminating on a live node" from "node confirmed gone".
- [ ] Used the out-of-service taint (and removed it afterwards) instead of ad hoc deletions.
- [ ] Confirmed the storage backend shows the volume detached from the dead node.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: RWO and RWOP semantics, Multi-Attach event text in the attach/detach controller source, non-graceful shutdown out-of-service taint and 6 minute force detach from the node shutdown docs.

Method: documentation only; no commands were run.
