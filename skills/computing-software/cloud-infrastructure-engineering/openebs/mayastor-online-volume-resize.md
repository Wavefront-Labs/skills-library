---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-online-volume-resize
name: mayastor-online-volume-resize
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, resize, allowvolumeexpansion, online, offline, pvc, expansion]
level: practitioner
status: docs-checked
description: "Expand a Mayastor volume by editing the PVC, online or offline, subject to dynamic provisioning, expansion-only, enough pool capacity and all replicas Online."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/re-resize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Mayastor CSI plugin can expand a dynamically provisioned PVC in both **online and offline** states, as long as the StorageClass has `allowVolumeExpansion: true`. That flag has been true by default in the Mayastor StorageClass since version 2.6.0. End users can edit the flag on the StorageClass.

Prerequisites listed on the page:

- only **dynamically provisioned** PVCs can be resized;
- only **expansion** is allowed, shrinking is not;
- the StorageClass that provisioned the PVC supports resize;
- the DiskPools that host the volume's replicas have sufficient capacity;
- **all replicas of the volume are Online**.

The page's example creates a class named `mayastor-1` with `protocol: nvmf`, `repl: "1"`, provisioner `io.openebs.csi-mayastor` and `allowVolumeExpansion: true`, creates a PVC, and then raises the size in the PVC spec.

After raising the PVC size (the example goes from 1Gi to 2Gi while a pod uses it), `kubectl get pvc` and `kubectl get pv` should show the new capacity.

**Known behaviour from the page.**

- For offline expansion of filesystem-mode volumes, the filesystem is expanded when the application pod starts and publishes the volume again. The node-expand request arrives about a second after the publish request, so an application that checks the filesystem size in that window sees the old size. Restarting the application pod mitigates it.
- If a volume is expanded during an upgrade while the IO engine is still outdated and lacks the fix for IO on an expanded volume, IO on the expanded range may fail. The page recommends waiting until the upgrade completes before expanding volumes.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown, advanced-operations resize page with doc id re-resize) in full. Prerequisites and the example match the page. Removed an invented troubleshooting order, the claims that a Degraded volume blocks expansion and that a volume cannot exceed pool size, and the DiskPool cross-reference; none are stated there. Added the page's known-behaviour notes.
