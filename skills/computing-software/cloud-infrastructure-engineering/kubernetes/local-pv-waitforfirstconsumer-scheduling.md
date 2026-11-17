---
id: computing-software.cloud-infrastructure-engineering.kubernetes.local-pv-waitforfirstconsumer-scheduling
name: local-pv-waitforfirstconsumer-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, local-raw-block-volumes, local-pv-scheduling, local-persistent-volumes, waitforfirstconsumer, volume-node-affinity]
level: practitioner
status: docs-checked
description: "Make pods using local PVs schedule correctly with WaitForFirstConsumer, PV nodeAffinity and capacity, and fix volume node affinity conflicts."
sources: ["https://kubernetes.io/docs/concepts/storage/volumes/#local", "https://kubernetes.io/docs/concepts/storage/storage-classes/#local", "https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling with local PVs

## The class
Local volumes can only be statically created PVs; dynamic provisioning is not supported. Still create a StorageClass so binding is delayed until a Pod is scheduled.
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: local-storage}
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```
With `WaitForFirstConsumer`, binding is delayed until a Pod using the PVC exists, and the scheduler can consider the Pod's resource requests, node selectors, affinity and taints while choosing a PV. With `Immediate`, binding happens at PVC creation without knowledge of the Pod's scheduling requirements, which can leave Pods unschedulable. Do not set `nodeName` on the Pod when using `WaitForFirstConsumer`.

## The PV declares its node
```yaml
apiVersion: v1
kind: PersistentVolume
metadata: {name: local-pv-worker-07}
spec:
  capacity: {storage: 100Gi}
  volumeMode: Filesystem
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local: {path: /mnt/disks/ssd1}
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - {key: kubernetes.io/hostname, operator: In, values: [worker-07]}
```
The system knows the volume's node constraint from the PV node affinity. If the node becomes unhealthy the volume is inaccessible and the Pod cannot run; applications must tolerate that availability and possible data loss.

## Pending Pod messages (scheduler volume binding plugin)
| Message | Meaning |
|---|---|
| `node(s) didn't find available persistent volumes to bind` | no unbound matching PV on the candidate nodes |
| `node(s) didn't match PersistentVolume's node affinity` | the PVC is already bound to a PV whose node affinity excludes the node (older releases worded this "volume node affinity conflict") |
| `node(s) did not have enough free storage` | storage capacity tracking reports not enough space |

## StatefulSet after node loss
The Pod's PVC is bound to a PV on the failed node and cannot schedule elsewhere. After confirming the node and disk are gone, delete the PVC (and the PV object) so a new claim can bind on another node, then let the application re-replicate (see `local-pv-disk-preparation-and-node-loss`).

## Verify
`kubectl get pvc -o wide` shows each PVC bound to a PV whose node matches the Pod's `spec.nodeName`.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: local volume rules, no-provisioner class, WaitForFirstConsumer behaviour, scheduler binding message constants in source.

Method: documentation only; no commands were run.
