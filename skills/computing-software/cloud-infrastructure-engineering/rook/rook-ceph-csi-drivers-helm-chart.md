---
id: computing-software.cloud-infrastructure-engineering.rook.rook-ceph-csi-drivers-helm-chart
name: rook-ceph-csi-drivers-helm-chart
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [ceph-csi-drivers, ceph-csi-operator, helm, csi-addons, network-fencing, cephfsclienttype]
level: advanced
status: docs-checked
description: "Install the ceph-csi-drivers chart after the rook-ceph chart with the recommended values file, and apply CSI-Addons, fencing and replica overrides."
sources:
  - https://rook.io/docs/rook/latest-release/Helm-Charts/csi-drivers-chart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Ceph-CSI drivers chart installs the resources ceph-csi needs under the ceph-csi-operator. The `rook-ceph` operator chart must be installed first because it brings in the Ceph-CSI operator and CRDs.

The chart is published from the ceph-csi-operator Helm repository and must be installed with the recommended values file; the drivers fail if only the chart defaults are used. If installing into another namespace, replace every `rook-ceph` in that values file.
```
helm repo add ceph-csi-operator https://ceph.github.io/ceph-csi-operator
helm install ceph-csi-drivers --namespace rook-ceph ceph-csi-operator/ceph-csi-drivers \
  -f https://raw.githubusercontent.com/rook/rook/v1.21.1/deploy/charts/ceph-csi-drivers/values.yaml
```

Common customizations, passed with a further `-f values.yaml`:
- CSI-Addons sidecar: `operatorConfig.driverSpecDefaults.deployCsiAddons: true`.
- Network fencing, RBD driver only: `drivers.rbd.deployCsiAddons: true` and `drivers.rbd.enableFencing: true`. Auto-unfencing requires the CSI-Addons controller to be deployed separately.
- Controller plugin replicas: `operatorConfig.driverSpecDefaults.controllerPlugin.replicas: 2`.
- CephFS client type: `drivers.cephfs.cephFsClientType: fuse` for the FUSE client rather than the kernel client.

Each override links to a section of the Ceph-CSI drivers page that explains the feature in depth.

## Checked

2026-11-03. Confirmed against the Ceph CSI Drivers Helm chart page and its recommended values.yaml: the helm commands, deployCsiAddons, drivers.rbd.enableFencing, controllerPlugin replicas 2 and cephFsClientType fuse examples, and the install-order requirement. Removed: nothing.

Method: documentation only; no commands were run.
