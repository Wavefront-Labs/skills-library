---
id: computing-software.cloud-infrastructure-engineering.longhorn.create-volumes
name: create-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [create-volumes, storageclass, v2-volumes, static-provisioning, scheduling-error]
level: practitioner
status: docs-checked
description: "Create Longhorn V1, V2 replicated and V2 sharded volumes with StorageClasses, static provisioning, UI-created PV and PVC, and diagnose scheduling errors."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/create-volumes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: provision volumes through Kubernetes.

Access modes: RWO (default), RWOP, RWX; ROX is not supported.

V1: needs at least one filesystem disk. StorageClass `longhorn` uses provisioner `driver.longhorn.io`, `numberOfReplicas: "3"`, `staleReplicaTimeout: "2880"`, `fsType: "ext4"`. Optional `mkfsParams` (v1.4.0+), `backupTargetName` (v1.8.0+), `diskSelector`, `nodeSelector`, `recurringJobSelector`. Omitted parameters use global settings.

V2 replicated: needs the V2 engine enabled and block disks; `dataEngine: "v2"`, `dataLayout.type: "replicated"`, `dataLayout.mode: "raid1"` (default), `numberOfReplicas: "3"`, `fsType: "ext4"`.

V2 sharded (experimental, not for production): `dataLayout.type: "sharded"`, `dataLayout.mode: "erasureCoding"`, `dataLayout.dataChunks: "4"`, `dataLayout.parityChunks: "2"`, `dataLayout.stripSizeKB: "64"` (fixed at creation), `numberOfReplicas: "1"`, `dataLocality: "disabled"`. Needs at least `dataChunks + parityChunks` schedulable nodes (6 for 4+2).

Static provisioning: create a PV with a custom StorageClass name, then a PVC requesting that name; Kubernetes first looks for a PV with a matching label, then a StorageClass object.

UI-created volumes: set `storageClassName` on the PVC or PV; the default name is `longhorn-static` (Setting, General, Default Longhorn Static StorageClass Name). Delete Longhorn-created PVCs and PVs manually. An existing volume can be used by a new pod only if detached.

Creation failures (insufficient storage, unavailable disks or nodes, unmet tags, incompatible size): read the PV annotation `longhorn.io/volume-scheduling-error` with `kubectl describe pv <name>`; multiple causes are separated by semicolons.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/create-volumes/

Changed: sharded parameters now carry the dataLayout. prefix as on the page.

Method: documentation only; no commands were run.
