---
id: computing-software.cloud-infrastructure-engineering.google-cloud.filestore-and-managed-nfs
name: filestore-and-managed-nfs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, filestore, nfs, managed-nfs, filestore-basic, filestore-zonal, filestore-regional, filestore-enterprise, filestore-backups, filestore-snapshots, nfs-mount-options, gke-filestore-csi, shared-filesystem, parallelstore, netapp-volumes, file-storage]
level: practitioner
status: docs-checked
description: "Shared POSIX file storage on GCP: Filestore tiers and sizing, private services access, mount options, backups and snapshots, GKE Filestore CSI, NetApp Volumes and Parallelstore."
sources: ["https://cloud.google.com/filestore/docs/service-tiers", "https://cloud.google.com/filestore/docs/creating-instances", "https://cloud.google.com/filestore/docs/mounting-fileshares", "https://cloud.google.com/filestore/docs/backups", "https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/filestore-csi-driver", "https://cloud.google.com/netapp/volumes/docs/discover/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filestore and managed NFS

**Goal:** a shared filesystem that many VMs or pods mount read-write, sized for the IOPS
it needs, reachable only inside the VPC, and backed up.

## 1. Pick a tier
| Tier | Capacity | Availability | Use |
|---|---|---|---|
| Basic HDD / SSD | 1-63.9 TiB | zonal, no SLA on HDD | dev, home dirs, low IOPS |
| **Zonal** | 1-100 TiB, perf scales with size | zonal | HPC scratch, CI caches, media |
| **Regional** | see the service tiers page for capacity | synchronous replication across zones | production shared state (CMS uploads, SAP, render farms) |
| Enterprise (legacy name for regional) | 1-10 TiB | regional | same as regional |
Performance is proportional to capacity on Zonal/Regional — buy capacity for IOPS, not just bytes. Filestore supports NFSv3 and NFSv4.1; choose the protocol when you create the instance.

## 2. Create
```bash
gcloud filestore instances create shared-prod --location=europe-west1 --tier=REGIONAL \
  --file-share=name=share1,capacity=2TiB --network=name=prod-vpc,connect-mode=PRIVATE_SERVICE_ACCESS \
  --kms-key=projects/P/locations/europe-west1/keyRings/kr/cryptoKeys/filestore
```
- `connect-mode=PRIVATE_SERVICE_ACCESS` uses the VPC's private services access range (shared with Cloud SQL/Memorystore); required for Shared VPC service projects and Regional tier. `DIRECT_PEERING` (legacy) allocates its own /29 — avoid.
- Firewall: allow tcp/udp 111, 2046-2050 from client subnets to the Filestore range (PSA range) — rules are evaluated in the host VPC.
- Capacity can grow online (and shrink on Zonal/Regional within limits); tier cannot change — migrate with `rsync`/Storage Transfer.

## 3. Mount
```bash
sudo apt-get install -y nfs-common
sudo mkdir -p /mnt/shared && sudo mount -t nfs -o nconnect=4,hard,timeo=600,retrans=5 10.0.5.2:/share1 /mnt/shared
# /etc/fstab
10.0.5.2:/share1 /mnt/shared nfs nconnect=4,hard,timeo=600,retrans=5,_netdev 0 0
```
- `nconnect` (kernel ≥5.3) gives multiple TCP streams; `hard` so writes never silently fail; `_netdev` so boot waits for network.
- Export options: IP-based access control with `--file-share=...,nfs-export-options=[{access-mode=READ_WRITE,ip-ranges=[10.0.0.0/8],squash-mode=ROOT_SQUASH,anon-uid=65534}]`. Root squash on by default on newer tiers.

## 4. GKE
Enable the CSI driver (`--addons=GcpFilestoreCsiDriver`); StorageClass `provisioner: filestore.csi.storage.gke.io` with `tier: zonal|regional|basic-hdd`, `network`, and **multishare** (`multishare: "true"`) so one Filestore instance backs many small PVCs (10 shares × ≥100 GiB each) — otherwise every `ReadWriteMany` PVC provisions a full 1 TiB instance. Volume expansion and snapshots are supported via CSI.

## 5. Protect
- **Backups** (region-level, incremental, cross-region restore): `gcloud filestore backups create bk-$(date +%F) --instance=shared-prod --instance-location=europe-west1 --region=europe-west1`; schedule with Cloud Scheduler → Workflows (no native schedule on Basic; Backup and DR Service can manage schedules).
- **Snapshots** (Zonal/Regional): instant, same-instance, for quick rollback; not a backup.
- Restore to a *new* instance for testing, or in place (`backups restore --destination-instance`).

## 6. When Filestore is wrong
- Throughput >10 GB/s or millions of small files for HPC/AI → **Parallelstore** (DAOS) or Managed Lustre.
- SMB, snapshots-as-first-class, replication, NetApp tooling → **Google Cloud NetApp Volumes**.
- Object semantics / cheap / global → Cloud Storage with `gcsfuse` (read-mostly only).

## Gotchas
- NFS from a VM in another region works but latency makes it miserable; keep clients in-region.
- Private services access range too small = "range exhausted" when creating the 3rd managed service; allocate /20 upfront.
- File ownership: Filestore stores numeric UIDs; keep UID/GID consistent across clients (OS Login helps).
- Deleting a VPC peering for PSA while Filestore exists bricks access; Filestore does not block it.

## Verify
- [ ] `mount | grep share1` shows `vers=4.1` (Zonal/Regional) and `nconnect=4`; `fio` from two VMs hits the tier's documented throughput for the capacity.
- [ ] Backup appears with `state: READY`; restore to a test instance and diff a sample tree.
- [ ] GKE: two pods on different nodes write and read the same file through one `ReadWriteMany` PVC.
- [ ] Client outside the allowed `ip-ranges` gets `access denied by server`.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the regional capacity range and availability percentage, and the tier-by-protocol claim about NFS v4.1.

Method: documentation only; no commands were run.
