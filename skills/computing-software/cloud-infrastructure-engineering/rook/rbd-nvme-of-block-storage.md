---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-nvme-of-block-storage
name: rbd-nvme-of-block-storage
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [nvme-of, nvme-tcp, cephnvmeofgateway, nvmeof-pool, subsystemnqn, experimental]
level: sme
status: docs-checked
description: "Expose RBD volumes over NVMe/TCP with the CephNVMeOFGateway CRD, a .nvmeof metadata pool, the NVMe-oF CSI driver and in-cluster or external clients."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/nvme-of/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This feature is marked experimental and needs Ceph v20 (Tentacle) or later. It lets pods in the cluster and external clients use NVMe-oF initiators to reach RBD volumes. Both use cases share the common setup first.

Common setup:
1. Create a `CephNVMeOFGateway`. The operator creates one Service and one Deployment per gateway instance. NVMe-oF uses two pools: a metadata pool named `.nvmeof` (created with `spec.name: .nvmeof`) holding subsystem and namespace definitions, and a standard CephBlockPool for the data.
2. Create the CSI driver CR: `kubectl create -f deploy/examples/csi/nvmeof/driver.yaml`. Check `kubectl get pods -n rook-ceph | grep nvmeof` for a controller plugin and node plugin.
3. Create the data pool (`nvmeof-pool.yaml`: replicated size 3, `failureDomain: host`).

In-cluster: a StorageClass with provisioner `rook-ceph.nvmeof.csi.ceph.com` (prefixed with the operator namespace) and parameters `pool: nvmeof`, `subsystemNQN` (shared subsystem for all in-cluster PVCs), `nvmeofGatewayAddress`, `nvmeofGatewayPort: "5500"` and a `listeners` list of gateway hostnames. Then create the PVC and pod.

External clients, through LoadBalancer services: install `nvme-cli`, run `modprobe nvme-tcp`, and make sure the client reaches the gateway IP. Create a VolumeAttributesClass listing allowed host NQNs. The external StorageClass omits `subsystemNQN`; each PVC gets its own subsystem and clients find it with `nvme discover`.

## Checked

2026-11-03. Confirmed against the NVMe-oF page: experimental status, the CephNVMeOFGateway and .nvmeof pool, the CSI driver CR, StorageClass parameters including port 5500, and the external client steps with nvme discover and VolumeAttributesClass. Removed: nothing.

Method: documentation only; no commands were run.
