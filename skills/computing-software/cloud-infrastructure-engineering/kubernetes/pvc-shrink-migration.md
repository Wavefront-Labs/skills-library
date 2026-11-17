---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pvc-shrink-migration
name: pvc-shrink-migration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, volume-expansion, pvc-shrink, pvc-migration, pv-migrate]
level: practitioner
status: docs-checked
description: "Why PVCs cannot be shrunk, the exception for recovering failed expansions, and the copy-and-swap procedure to move data to a smaller volume."
sources: ["https://kubernetes.io/docs/concepts/storage/persistent-volumes/#recovering-from-failure-when-expanding-volumes", "https://github.com/utkuozdemir/pv-migrate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shrinking a PVC

## It is not supported
Kubernetes does not support shrinking a PVC below its current size: a requested size must stay above `.status.capacity`.

## The exception
If an expansion failed, you can lower the request to a smaller value that is still greater than `.status.capacity` (`RecoverVolumeExpansionFailure`, stable in 1.34). That cancels a failed expansion; it is not a shrink.

## Copy-and-swap procedure
1. Create the smaller PVC (for example `data-small`) in the same namespace.
2. Stop writers: scale the workload to 0.
3. Copy with `pv-migrate` (kubectl plugin installable with krew; it runs rsync or rclone inside the cluster):
```bash
kubectl pv-migrate --source data --dest data-small
```
or a Job that mounts both PVCs and runs rsync (`-a` archive, `-H` hard links, `-A` ACLs, `-X` xattrs, `--numeric-ids` to avoid uid/gid name mapping).
4. Point the workload at the new PVC and scale up. For StatefulSets the PVC name is derived from the template: delete the old PVC, recreate one with the original name at the new size, and copy data back (two copies), or recreate the StatefulSet with a new template name.
5. Keep the old PVC until verified, then delete it.

## Alternatives
- Database-level dump and restore into a fresh volume.
- `pv-migrate backup` and `restore` through object storage.

## Verify
Compare file counts, sizes and checksums for critical data between source and target before deleting the original.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) plus the named upstream project docs and Kubernetes source. Confirmed: no shrinking below status.capacity, failed-expansion exception, pv-migrate role, rsync flags in the rsync manual.

Method: documentation only; no commands were run.
