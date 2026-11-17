---
id: computing-software.cloud-infrastructure-engineering.kubernetes.shared-emptydir-between-containers
name: shared-emptydir-between-containers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, init-containers, shared-emptydir, emptydir, sidecar]
level: practitioner
status: docs-checked
description: "Share files between init, sidecar and app containers with an emptyDir: mounting, permissions, sizeLimit, write ordering and common patterns."
sources: ["https://kubernetes.io/docs/tasks/access-application-cluster/communicate-containers-same-pod-shared-volume/", "https://kubernetes.io/docs/concepts/storage/volumes/#emptydir", "https://kubernetes.io/docs/concepts/storage/ephemeral-storage/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Sharing an emptyDir between containers

```yaml
spec:
  volumes:
  - name: shared
    emptyDir:
      sizeLimit: 500Mi
  initContainers:
  - name: fetch-config
    image: busybox:1.28
    command: ["sh", "-c", "wget -qO /work/app.conf http://config-svc/app.conf"]
    volumeMounts: [{name: shared, mountPath: /work}]
  containers:
  - name: app
    image: app:1.0
    volumeMounts: [{name: shared, mountPath: /etc/app, readOnly: true}]
  - name: log-shipper
    image: <shipper-image>
    volumeMounts: [{name: shared, mountPath: /logs, subPath: logs}]
```

## How it behaves
The volume is created when the Pod is assigned to a node and starts empty. All containers in
the Pod can read and write the same files, and it can be mounted at the same or different paths
in each container. Data survives container crashes (a crash does not remove the Pod from the
node) but is deleted permanently when the Pod is removed from the node for any reason.

## Patterns
- Init container renders or downloads files, app reads them (the docs show an init container
  cloning a Git repository into an emptyDir, and templating a config file).
- A content-manager container fetches files while a web server container serves them (the
  shared-volume task example); scratch space; checkpointing a long computation.
- App writes logs or reports, a sidecar ships them.

## Permissions
- Without `emptyDir.mode` the directory is created with `0777`; `emptyDir.mode` (a field behind a
  feature gate; see the Volumes page for its stage) sets Unix permission bits from `0000` to `01777`.
  If `fsGroup` is set in the Pod securityContext, its group permissions override `mode`.
- `fsGroupChangePolicy` has no effect on `emptyDir`.
- `readOnly: true` on consumer mounts prevents accidental writes.

## Ordering
- Init containers finish before app containers start: a safe handoff.
- Between regular app containers the docs describe no start ordering, so the reader must tolerate
  missing files; a native sidecar with a `startupProbe` can hold later containers back.
- Write to a temporary name and rename so readers do not see partial files (general file-system
  practice, not a Kubernetes guarantee).

## Limits
- By default the volume lives on whatever medium backs the node; `medium: Memory` mounts a tmpfs
  whose files count against the memory limit of the container that wrote them (unsized
  memory-backed volumes are sized to node allocatable memory).
- `sizeLimit` bounds the capacity; storage is allocated from node ephemeral storage, so the
  volume can run out of room before the limit if the node's ephemeral storage fills from
  other sources. Non-tmpfs `emptyDir` usage counts toward the Pod's local ephemeral-storage
  limit, and the kubelet marks a Pod for eviction when the summed usage exceeds the Pod limit.
- Not for data that must survive rescheduling.

## Verify
```bash
kubectl exec <pod> -c app -- ls -l /etc/app
kubectl exec <pod> -c log-shipper -- df -h /logs
```

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Volumes" (emptyDir), "Ephemeral Storage",
"Init Containers", "Sidecar Containers" and the shared-volume task (latest release v1.37.1).
Confirmed: lifecycle and crash behaviour, medium, `sizeLimit` semantics, `mode` default and
`fsGroup` interaction, eviction on pod-level overflow, `fsGroupChangePolicy` limitation. Replaced
the unnamed log-shipper image and removed the unconfirmed "exceeding sizeLimit evicts the pod"
claim.
Method: documentation only; no commands were run.
