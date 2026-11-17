---
id: computing-software.cloud-infrastructure-engineering.openebs.lvm-volumeattributesclass-qos-limits
name: lvm-volumeattributesclass-qos-limits
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, lvm, volumeattributesclass, vac, qos, iops, bandwidth, cgroup-v2, kubernetes-1-34]
level: advanced
status: docs-checked
description: "Apply IOPS and bandwidth limits to Local PV LVM volumes with a VolumeAttributesClass: parameter names, max and size suffixes, unified versus directional settings, Kubernetes 1.34."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/configuration/lvm-create-vac
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-lvm/configuration/lvm-vac-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A VolumeAttributesClass (VAC) defines mutable Quality of Service parameters for Local PV LVM volumes. It limits IOPS and bandwidth for both filesystem and block-mode volumes, enforced at node level with Linux **cgroup v2** controls. It needs a Kubernetes release that has the VAC API, which the guide lists as 1.34 and later. On older clusters everything else works but the VAC configuration is ignored. When a VAC is attached to a PVC the driver applies the QoS to the volume, and VAC updates are reconciled automatically on supported versions.

Parameters:

| Parameter | Meaning |
|---|---|
| `qosIopsLimit` | combined read/write IOPS |
| `qosIopsReadLimit`, `qosIopsWriteLimit` | per direction IOPS |
| `qosBandwithPerSec` | combined bandwidth |
| `qosBandwithReadPerSec`, `qosBandwithWritePerSec` | per direction bandwidth |

IOPS values are non-zero positive integers or `max`, which disables limiting for that parameter. Bandwidth values are bytes per second or a size suffix such as `7000Mi`. Zero is not supported. Note the documented spelling `Bandwith` (without the d): names are **case-sensitive**, a misspelled or recased name is rejected as unsupported, and values must not have leading or trailing spaces.

The unified parameters (`qosIopsLimit`, `qosBandwithPerSec`) apply to both directions unless the matching directional parameter is also set. Apply the VAC with `kubectl apply -f vac.yaml` and list it with `kubectl get volumeattributesclass`. To change the policy, point the PVC's `volumeAttributesClassName` at another VAC; only parameters present in the new VAC are applied, so set a parameter to `max` instead of omitting it to remove a limit.

## Checked

2026-11-04. Confirmed against the Create VolumeAttributesClass and Local PV LVM VAC Parameters pages: the six parameter names and accepted values, `max`, cgroup v2, case-sensitivity, Kubernetes 1.34 and later, unified versus directional behaviour, and the update behaviour added above. Removed the generic advice to copy manifests.

Method: documentation only; no commands were run.
