---
id: computing-software.cloud-infrastructure-engineering.kubernetes.readwriteonce-multi-pod-same-node
name: readwriteonce-multi-pod-same-node
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, access-modes, rwo-multi-pod, readwriteonce, readwriteoncepod]
level: practitioner
status: docs-checked
description: "ReadWriteOnce allows several pods on the same node to mount a volume; use ReadWriteOncePod when exactly one pod must write, and how this bites rolling updates."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes", "https://kubernetes.io/blog/2023/12/18/read-write-once-pod-access-mode-ga/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ReadWriteOnce is per node

## Semantics
- `ReadWriteOnce` (RWO): mountable read-write by a single node; any number of Pods on that node may use it at the same time.
- `ReadWriteOncePod` (RWOP, stable in 1.29): read-write by a single Pod across the whole cluster. Only for CSI volumes (Kubernetes 1.22 or later, with csi-provisioner v3.0.0+, csi-attacher v3.3.0+ and csi-resizer v1.3.0+).
- Access modes are used for matching and sometimes constrain where a volume can mount; they do not enforce write protection after the volume is mounted (apart from RWOP, which constrains the volume to one Pod). A volume is mounted with one access mode at a time.

## Where it surprises people
- Two replicas of a Deployment sharing an RWO PVC both run if scheduled on the same node; on different nodes the second waits for the attach (Multi-Attach error).
- A rolling update with a surge Pod can place the new Pod on the same node (both run at once) or on another node (waits until the old Pod releases the volume).

## Choosing
| Need | Mode or pattern |
|---|---|
| Exactly one Pod may use the volume | RWOP |
| One replica with RWO | Deployment with `strategy.type: Recreate` |
| Per-Pod storage | StatefulSet with `volumeClaimTemplates` |
| Shared files across nodes | a volume type that supports ReadWriteMany |

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata: {name: data}
spec:
  accessModes: [ReadWriteOncePod]
  storageClassName: <csi-storage-class>
  resources: {requests: {storage: 20Gi}}
```

## Verify
```bash
kubectl get pods -o wide -l app=db
kubectl describe pod <stuck-pod>
```

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: RWO per node, RWOP stable in 1.29 and CSI-only requirements, access-mode caveats.

Method: documentation only; no commands were run.
