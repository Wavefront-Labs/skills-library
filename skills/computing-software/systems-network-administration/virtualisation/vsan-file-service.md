---
id: computing-software.systems-network-administration.virtualisation.vsan-file-service
name: vsan-file-service
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan-file-service, nfs, smb, file-shares, vsan, vmware, vsphere]
level: advanced
status: docs-checked
description: "Deploy vSAN File Service to serve NFS and SMB shares from a vSAN cluster: IP pool, AD join for SMB, share quotas and permissions, and health checks."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0/vsan-administration/expanding-and-managing-a-vsan-cluster/vsan-file-service/enable-vsan-file-service.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0/vsan-administration/expanding-and-managing-a-vsan-cluster/vsan-file-service/limitations-and-considerations-of-vsan-file-service.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vSAN File Service

**Goal:** NFS v3/v4.1 and SMB shares backed by vSAN, managed in vCenter, without a separate filer.

## Prerequisites
- vSAN cluster (OSA or ESA; vSAN 8.0 supports stretched clusters and two-node
  configurations).
- One static IP per file server (vSAN 8.0 supports 64 file servers in a 64-host setup) with forward and reverse DNS.
- A distributed port group for file service traffic; on vDS enable **MAC learning and forged transmits** (the wizard does it on vDS; on standard switches set promiscuous+forged transmits).
- For SMB and Kerberos NFS: an AD domain, OU and service account that can join computers.

## Enable
Cluster -> Configure -> vSAN -> Services -> File Service -> Enable: download/upload the file service agent OVF (online or offline), domain name, DNS, IP pool. vSAN deploys one agent VM per host (protected, do not touch them).

## Create shares
File Shares -> Add: name, protocol (NFS 3, 4.1, both, or SMB), storage policy (FTT applies), **quota** (warning and hard), labels. NFS: net access control (client IP ranges, root squash). SMB: set share permissions from Windows (Computer Management against the file server name).

## Use
```sh
mount -t nfs -o vers=4.1 fs01.example.com:/vsanfs/share1 /mnt/share1
```
SMB: `\\fs01.example.com\share1`. Kubernetes uses File Service for RWX persistent volumes via CNS.

## Gotchas
- Agent VMs are not migrated by DRS like normal VMs; host maintenance mode moves the file server container to another host (short pause).
- Do not use File Service shares as vSphere datastores; not supported.
- Snapshots (8.0) via API/Veeam; no user-facing previous versions on older builds.

## Verify
vSAN health *File Service* checks green; shares mount from clients; failover tested by putting a host in maintenance mode.

## Checked
2026-10-31: Confirmed NFS v3/v4.1 and SMB protocols, the enable workflow, agent VMs, share
quotas and NFS access control against the vSAN 8.0 "Enable vSAN File Service" page; the
64-file-server / 64-host limit, 100 file shares and stretched/two-node support against
the "Limitations and Considerations of vSAN File Service" page. Corrected the file-server
limit (32 -> 64), replaced the dead core.vmware.com tech note, and removed the 8.0U1 ESA
and 7.0U2 stretched version claims.
Method: documentation only; no commands were run.
