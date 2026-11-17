---
id: computing-software.cloud-infrastructure-engineering.google-cloud.filestore-networking-scaling-replication-and-multishare
name: filestore-networking-scaling-replication-and-multishare
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, filestore, filestore-ip-ranges, filestore-private-services-access, filestore-capacity-scaling, filestore-resize, filestore-replication, filestore-dr, filestore-multishare, multishare-csi]
level: advanced
status: docs-checked
description: "Operate Filestore: connect modes and reserved IP ranges, scaling capacity per tier, promoting a replica, and multishare for GKE."
sources: ["https://docs.cloud.google.com/filestore/docs/creating-instances", "https://docs.cloud.google.com/filestore/docs/scale", "https://docs.cloud.google.com/filestore/docs/optimize-multishares", "https://file.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filestore: networking, scaling, replication and multishare

## 1. Networking
`--network=name=...,connect-mode=...` selects how clients reach the instance. Per the Filestore API
(`NetworkConfig.connectMode`) the values are `DIRECT_PEERING` (the default when unset),
`PRIVATE_SERVICE_ACCESS` (private services access: the range comes from your allocated range) and
`PRIVATE_SERVICE_CONNECT` (needs a connection policy in the region).

Reserved IP range block size (Creating instances page): basic instances need a /29 block (for example
`10.123.123.0/29`); zonal, regional and enterprise instances need a /26 block.
```bash
gcloud filestore instances create nfs-prod --zone=<ZONE> --tier=<TIER> \
  --file-share=name=vol1,capacity=1TiB \
  --network=name=prod,reserved-ip-range=<CIDR_OR_RANGE_NAME>
```
Enterprise instances take a region as location; all other tiers take a zone.

## 2. Scaling
```bash
gcloud filestore instances update nfs-prod --zone=<ZONE> --file-share=name=vol1,capacity=2TiB
```
From the Scale capacity page: scaling does not affect availability and can be done while the instance
is in use. Basic HDD and Basic SSD scale up only; zonal, regional and enterprise tiers scale up and
down. You cannot scale below what the existing data and metadata need (an error), and while a scale
operation runs you cannot cancel it or edit the instance. Zonal higher-capacity instances can take longer
than enterprise and basic, so scale ahead of need. File share names cannot change after creation.
Each file uses one inode, and the only way to add inodes is to add capacity (check with `df -i`).

## 3. Replication and DR
- **Backups**: `gcloud filestore backups create b1 --instance=nfs-prod --instance-zone=<ZONE> --file-share=vol1 --region=<REGION>`.
- **Replica promotion**: the Filestore API has `instances.promoteReplica` ("Promote the standby
  instance (replica)"), exposed as `gcloud filestore instances promote-replica`. Repoint clients to the promoted instance.
- Check the replication and tier support pages for which tiers support replicas before you design a DR plan.

## 4. Multishare for GKE
Multishare is an enterprise-tier feature of the GKE Filestore CSI driver: many PVCs (shares) are packed
onto one Filestore instance. The GKE-provided StorageClass `enterprise-multishare-rwx` creates instances
that support up to 10 shares. A custom class sets `multishare: "true"` and `tier: enterprise`;
`max-volume-size: "128Gi"` maps up to 80 shares, each 10 GiB to 128 GiB, to one 10 TiB enterprise
instance. The minimum share size is 10 GiB.
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: filestore-multishare}
provisioner: filestore.csi.storage.gke.io
parameters: {tier: enterprise, multishare: "true", max-volume-size: "128Gi"}
allowVolumeExpansion: true
```
Enable the GKE Filestore CSI driver on the cluster first.

## Gotchas
- Pick reserved ranges that do not overlap other ranges in your network.
- Check the Filestore quotas and limits pages for share counts per instance.

## Verify
- [ ] `gcloud filestore instances describe nfs-prod --zone=<ZONE> --format='yaml(networks,fileShares,tier)'` matches design.
- [ ] A DR drill restores the latest backup (or promotes the replica) and a client mounts it.

## Checked
2026-10-28. Confirmed against the Filestore Creating instances page (/29 and /26 block sizes), the Scale
capacity page (directions, behaviour, inodes, location rule), the Optimize multishares page
(`enterprise-multishare-rwx`, 10 shares, 80 shares at 128Gi, 10 GiB minimum) and the Filestore API v1
discovery document (connect modes, default, `promoteReplica`). Commands were checked against the gcloud
reference. Removed: NFS port list, per-tier shrink claims, RPO figure, regional-tier failure claim, restore
scope, export-option and IAM claims, cost claim, and the CSI add-on flag (not confirmed).
Method: documentation only; no commands were run.
