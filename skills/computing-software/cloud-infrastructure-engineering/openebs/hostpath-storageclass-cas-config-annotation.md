---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-storageclass-cas-config-annotation
name: hostpath-storageclass-cas-config-annotation
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, storageclass, cas-config, basepath, filepermissions, reclaim-policy, annotations]
level: practitioner
status: docs-checked
description: "Configure Local PV Hostpath via the cas.openebs.io/config annotation, not parameters: StorageType, BasePath, NodeAffinityLabels, FilePermissions, quotas, binding mode."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/configuration/hostpath-storageclass-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local PV Hostpath uses an out-of-tree provisioner and **does not use the StorageClass `parameters` field**. Its settings go in the `cas.openebs.io/config` annotation, next to `openebs.io/cas-type: local`. Each entry has a `name` and takes `value`, `data` or `list`.

Required StorageClass fields: `provisioner: openebs.io/local` and `volumeBindingMode: WaitForFirstConsumer`. With `Immediate`, no node is chosen at provision time and the PVC stays pending. `reclaimPolicy` may be `Delete` (default) or `Retain`; Retain keeps the directory and its data after the claim is deleted. `allowedTopologies` is also supported.

Supported config names:

| Name | Form | Meaning |
|---|---|---|
| `StorageType` | value | `hostpath` |
| `BasePath` | value | absolute node path; default is the install-time path, `/var/openebs/local` |
| `NodeAffinityLabels` | list | label keys identifying the node instead of hostname |
| `FilePermissions` | data (`mode`) | permissions of the volume directory; default `0777` |
| `XFSQuota`, `EXT4Quota` | data | `softLimitGrace`, `hardLimitGrace` |

Each volume gets its own subdirectory named after the PV. A missing `BasePath` directory is created when the first volume lands on the node. `FilePermissions` applies only when a directory is created, so existing volumes are unaffected.

## Checked

2026-11-04. Confirmed against the Local PV Hostpath StorageClass Parameters page: the annotation mechanism, required fields, config names and forms, defaults, and the BasePath and FilePermissions behaviour. Narrowed the binding-mode sentence to what the page says about `Immediate` and removed generic advice.

Method: documentation only; no commands were run.
