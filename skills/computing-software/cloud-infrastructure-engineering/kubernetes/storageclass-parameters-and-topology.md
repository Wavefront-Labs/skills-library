---
id: computing-software.cloud-infrastructure-engineering.kubernetes.storageclass-parameters-and-topology
name: storageclass-parameters-and-topology
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, storageclass, provisioner, parameters, topology, allowedtopologies, ebs-csi, gce-pd-csi, azure-disk-csi, gp3, io2, regional-pd, premium-ssd, zonal, multi-zone, volumebindingmode]
level: advanced
status: docs-checked
description: "StorageClass provisioner parameters for AWS/GCP/Azure CSI drivers and how allowedTopologies + volumeBindingMode control which zone a disk lands in."
sources: ["https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode", "https://kubernetes.io/docs/concepts/storage/storage-classes/#allowed-topologies", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/parameters.md", "https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver", "https://github.com/kubernetes-sigs/azuredisk-csi-driver/blob/master/docs/driver-parameters.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StorageClass parameters and topology — picking the right disk, in the right zone

**Goal:** choose provisioner parameters that match the workload's IOPS/throughput
need, and guarantee the disk lands where the pod can actually attach it.

## 1. Per-cloud parameter cheatsheet (CSI drivers, not in-tree)
**AWS (`ebs.csi.aws.com`)**
```yaml
parameters:
  type: gp3            # driver default gp3; also io1, io2, gp2, sc1, st1, standard
  iops: "4000"          # io1, io2 and gp3 volumes
  throughput: "250"     # gp3 only, MiB/s; default 125
  encrypted: "true"
  kmsKeyId: "<KMS_KEY_ARN>"
```
**GCP (`pd.csi.storage.gke.io`)**
```yaml
parameters:
  type: pd-ssd                # driver default pd-standard; any PD type, e.g. pd-ssd, pd-balanced
  replication-type: none       # none (default) or regional-pd
  provisioned-iops-on-create: "10000"   # IOPS to provision; see GCP docs for which disk types accept it
```
For a regional PD in a zonal cluster, `allowedTopologies` must name two zones, one of them the
cluster's zone. In a regional cluster you can omit `allowedTopologies` and the driver picks two zones
from the cluster's region (per the GCP PD CSI driver user guide).
**Azure (`disk.csi.azure.com`)**
```yaml
parameters:
  skuName: Premium_LRS        # also Standard_LRS, StandardSSD_LRS, UltraSSD_LRS, Premium_ZRS, StandardSSD_ZRS, PremiumV2_LRS
  cachingMode: ReadOnly       # None, ReadOnly (driver default) or ReadWrite (deprecated)
  # DiskIOPSReadWrite / DiskMBpsReadWrite apply to UltraSSD and PremiumV2_LRS (see the driver parameter table)
```
`UltraSSD_LRS` and `PremiumV2_LRS` only support `cachingMode: None`; see the Azure Disk CSI driver
parameter table for the other constraints.

## 2. Topology-aware provisioning
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: fast-multi-az}
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowedTopologies:
- matchLabelExpressions:
  - key: topology.kubernetes.io/zone
    values: [us-east-1a, us-east-1b]
```
- `allowedTopologies` restricts which zones the provisioner is even allowed to pick —
  use it to keep disks (and their cost) out of a zone you don't run nodes in.
- `volumeBindingMode: WaitForFirstConsumer` delays binding and provisioning until a pod using the claim
  exists, so the volume is provisioned conforming to the pod's scheduling constraints. The EBS CSI driver
  documentation recommends it whenever possible. `Immediate` binding provisions without knowledge of
  the pod's scheduling requirements, which may result in unschedulable pods (the scheduler reports
  `node(s) didn't match PersistentVolume's node affinity` when a PV's node affinity excludes a node).

## 3. Matching parameters to the workload
Pick the volume type and its IOPS/throughput parameters from the driver's parameter table and the
cloud's own volume-type documentation, not from rules of thumb; for latency-sensitive services such
as etcd, see `computing-software.cloud-infrastructure-engineering.kubernetes.etcd-storage-requirements`.
The file system type is set with the `csi.storage.k8s.io/fstype` parameter (EBS CSI driver: `ext4` default,
also `xfs` and `ext3`).

## Gotchas
- Parameter keys are defined by each driver; the API only limits a StorageClass to 512 parameters and
  256 KiB in total. Check the driver's parameter table.
- Changing a StorageClass's parameters is not possible (parameters are immutable, see
  `computing-software.cloud-infrastructure-engineering.kubernetes.storageclass-immutability-and-replacement`),
  and existing PVs keep what they were provisioned with.
- Requested IOPS above the maximum for the volume type are capped by the EBS CSI driver; below the minimum
  they return an error by default. Specify either `iops` or `iopsPerGb`, not both. Read the current driver
  docs rather than assuming request values are honoured verbatim.

## Verify
- [ ] Looked up the parameters for the chosen disk type in the driver's parameter table.
- [ ] A `WaitForFirstConsumer` class with `allowedTopologies` provisioned a disk only
      in the zone the pod actually scheduled to.
- [ ] Explained why `Immediate` binding can produce a PV whose node affinity excludes the pod's nodes.

## Checked

2026-10-23, against the Kubernetes documentation (kubernetes/website main, v1.37 era) and the kubernetes-csi docs. Confirmed from each driver's parameter documentation: EBS (type values and gp3 default, iops for io1/io2/gp3, throughput gp3-only default 125, encrypted, kmsKeyId, csi.storage.k8s.io/fstype ext4 default, iops vs iopsPerGb, capping behaviour, WaitForFirstConsumer recommendation); GCE PD (type default pd-standard, replication-type none/regional-pd, provisioned-iops-on-create, regional PD allowedTopologies rules); Azure Disk (skuName values, cachingMode default ReadOnly, UltraSSD/PremiumV2 caching limits, DiskIOPSReadWrite/DiskMBpsReadWrite). Kubernetes docs: Immediate vs WaitForFirstConsumer, 512 parameter/256 KiB limit; scheduler message from binder.go. Corrected: regional PD zones are picked by the driver in regional clusters, `pd-extreme` is not listed in the driver docs, the volume node affinity message wording, and the fsType parameter name. Removed unconfirmed workload-sizing advice, the AKS ultra-disk node-pool claim, 'regional disks need no WaitForFirstConsumer' and the 3000 IOPS pricing claim.

Method: documentation only; no commands were run.
