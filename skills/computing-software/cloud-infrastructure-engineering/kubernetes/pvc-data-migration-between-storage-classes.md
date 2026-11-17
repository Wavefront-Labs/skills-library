---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pvc-data-migration-between-storage-classes
name: pvc-data-migration-between-storage-classes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pv-migrate, pvc-migration, storage-class-migration, statefulset, rsync, storage]
level: advanced
status: docs-checked
description: "Move data from one PVC to another (new StorageClass, namespace or cluster) with pv-migrate or an rsync Job, including the StatefulSet orphan-and-recreate cutover."
sources: ["https://github.com/utkuozdemir/pv-migrate", "https://github.com/utkuozdemir/pv-migrate/blob/main/docs/migrate.md", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/", "https://kubernetes.io/docs/tasks/run-application/delete-stateful-set/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating data between PVCs and storage classes

## When
Changing volume type, moving to another namespace or cluster, or moving to a different StorageClass: the data lives in the backend, there is no built-in way to move it, and a StorageClass cannot be edited on an existing PVC, so create a new PVC and copy.

## Option A: pv-migrate
`pv-migrate` copies one PVC into another (same namespace, across namespaces or clusters) with rsync inside the cluster; it is installable with Homebrew, krew, Scoop, release archives or Docker.
```bash
pv-migrate --source old-pvc --dest new-pvc
pv-migrate --source-namespace source-ns --source old-pvc --dest-namespace dest-ns --dest new-pvc
pv-migrate --source-kubeconfig <src-kubeconfig> --source-context <ctx> --source-namespace source-ns --source old-pvc \
  --dest-kubeconfig <dst-kubeconfig> --dest-context <ctx> --dest-namespace dest-ns --dest new-pvc
```
Strategies are tried in order (`--strategies` overrides): `mount` (both PVCs mounted in one Pod, same namespace only), `clusterip` (rsync over SSH through a ClusterIP Service, same cluster), `loadbalancer` (LoadBalancer Service, works across clusters when reachable), and the opt-in `nodeport` and `local` (tunnels through your machine; recommended for smaller transfers only). Other flags documented: `--rsync-extra-args`, `--dest-delete-extraneous-files`, `--detach` for large transfers, `--rsync-push` when the source cannot expose a service, `--helm-set` for chart overrides. Re-running copies deltas, so do a warm copy and a final copy after stopping writers. If files vanish from the source during the transfer rsync skips them with a warning.

## Option B: your own rsync Job
```yaml
apiVersion: batch/v1
kind: Job
metadata: {name: copy-data, namespace: db}
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: rsync
        image: <image-with-rsync>
        command: ["rsync", "-aHAX", "--numeric-ids", "/src/", "/dst/"]
        volumeMounts: [{name: src, mountPath: /src, readOnly: true}, {name: dst, mountPath: /dst}]
      volumes:
      - {name: src, persistentVolumeClaim: {claimName: data-old}}
      - {name: dst, persistentVolumeClaim: {claimName: data-new}}
```
`-a` is archive mode (without ACLs, xattrs or hard links, which `-A`, `-X` and `-H` add); `--numeric-ids` skips uid/gid name mapping. Both PVCs must be mountable by one Pod (RWO volumes are attached per node); otherwise use a pv-migrate network strategy.

## StatefulSet cutover (volumeClaimTemplates cannot be updated)
1. Set old PVs to `Retain`: `kubectl patch pv <pv> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'`.
2. `kubectl scale sts db --replicas=0` and wait for the Pods to go.
3. Copy each `data-db-N` into a new PVC on the new class; delete the old `data-db-N` PVCs and create new ones with the same names on the new class (StatefulSet PVCs are named `<template>-<statefulset>-<ordinal>`).
4. `kubectl delete sts db --cascade=orphan`; apply the StatefulSet with the new `storageClassName`; scale up.

## Verify
- [ ] File counts and sizes match; run application-level checks for databases.
- [ ] Old PVs stay `Retain` until the app has run on the new volumes for an agreed period.

## Gotchas
- Copying a live database file by file can produce a corrupt copy; stop writes or use the database's own dump or replication.
- Preserve ownership (`--numeric-ids`) or Pods may hit permission errors under a different `fsGroup`.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: pv-migrate strategy names, flags and workflows, rsync flags, StatefulSet orphan cutover.

Method: documentation only; no commands were run.
