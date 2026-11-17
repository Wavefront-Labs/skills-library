---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-pvc-pending-and-access-mode
name: hostpath-pvc-pending-and-access-mode
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, pvc, pending, waitforfirstconsumer, readwriteonce]
level: intro
status: docs-checked
description: "Create a Local PV Hostpath PVC, expect it to stay Pending until a pod is scheduled, remember it supports ReadWriteOnce only, and use PVC annotations for per-volume settings."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/configuration/hostpath-create-pvc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Local PV Hostpath claim names a hostpath StorageClass (default `openebs-hostpath`), asks for a size, and requests `ReadWriteOnce`. Create it with `kubectl apply -f local-hostpath-pvc.yaml` and inspect it with `kubectl get pvc local-hostpath-pvc`.

Two behaviours surprise newcomers:

- **Pending is normal.** Hostpath classes use `volumeBindingMode: WaitForFirstConsumer` because the directory must be created on the node where the pod runs. Kubernetes picks the node first, and the provisioner then creates the volume and the claim becomes Bound with a `pvc-...` volume name. Deploy a pod that uses the claim to see it bind.
- **ReadWriteOnce only.** A PVC requesting any other access mode is not provisioned.

An individual PVC can also carry configuration through the `cas.openebs.io/config` annotation, which takes the same entries as the StorageClass. This is useful when one volume needs a setting that differs from others using the same class. The page's example sets `FilePermissions` with `mode: "0770"`.

**Precedence.** The StorageClass configuration wins. A PVC annotation only applies for parameters the StorageClass does not already set, so it cannot override a value the class defines.

**BasePath.** A `BasePath` supplied in a PVC annotation is ignored by default, because any user who can create PVCs in a namespace could otherwise choose a directory on the node. The provisioner flag `--allow-insecure-pvc-basepath-override` (Helm: `localpv-provisioner.localpv.allowInsecurePvcBasePathOverride: true`) re-enables it. The page warns to leave it disabled unless needed and to set `BasePath` on the StorageClass instead.

The page's verify section shows the claim Pending before a pod using it is scheduled, and Bound afterwards.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for hostpath-create-pvc) in full. Removed two unsourced statements (existing volumes unchanged after annotation edits; a diagnosis order). Added the annotation precedence and BasePath rules the page states.
