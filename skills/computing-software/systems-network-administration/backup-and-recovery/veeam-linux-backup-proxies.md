---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-linux-backup-proxies
name: veeam-linux-backup-proxies
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-linux-proxy, backup-proxy, hotadd, direct-san, transport-mode]
level: advanced
status: docs-checked
description: "Deploy Veeam backup proxies on Linux for VMware: which Linux servers can be proxies, transport modes and their order, and where to place proxies."
sources:
  - https://helpcenter.veeam.com/docs/vbr/userguide/backup_proxy.html
  - https://helpcenter.veeam.com/docs/vbr/userguide/transport_modes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam Linux backup proxies

A VMware backup proxy sits between the backup server and the rest of the infrastructure: it retrieves VM data from production storage, compresses, deduplicates and encrypts it, and sends it to the repository (or another proxy for replication). A proxy can be a Windows-based or Linux-based server added to Veeam Backup & Replication and given the VMware backup proxy role.

## Deploy
1. Add the Linux server as a managed server, then assign it the VMware backup proxy role.
2. By default the backup server itself is the proxy, which is enough only for small installations; deploy dedicated proxies for large ones. Several proxies share the workload, in the primary site and remote sites.
3. Which Linux servers can be proxies (13.1.2.57 table): a Linux server added with **persistent credentials** supports Direct storage access (Direct SAN with iSCSI, FC, NFS, NVMe-FC, NVMe-TCP, NVMe-RDMA), Virtual appliance and Network modes. A Linux server added with single-use credentials as a Hardened Repository supports Network mode only. The Veeam Software Appliance supports only Virtual appliance and Network mode.

## Transport modes (most efficient first)
| Mode | Placement guidance from the docs |
|---|---|
| Direct storage access | FC SAN: physical proxy with direct FC access. iSCSI/NFS: physical or virtual proxy. Not supported on vSAN |
| Virtual appliance (HotAdd) | Proxy is a VM on an ESXi host connected to the storage; with local storage, a proxy VM on every ESXi host |
| Network | Any machine on the storage network; not recommended on 1 Gb Ethernet, works well on 10 Gb |

- Automatic selection picks in the order Direct storage access, Virtual appliance, Network. You can instead choose the mode in the proxy settings.
- With VMware Cloud on AWS the only available mode is Virtual appliance.
- If storage is added to the console, Backup from Storage Snapshots is also possible.

## Verify
Check the job statistics for the transport mode actually used and compare with the intended one.

## Checked
2026-11-09. Read in full: Veeam Help Center "VMware Backup Proxies" and "Transport Modes" (build 13.1.2.57). Corrected: single-use credentials do not give a full proxy (the page lists them as Hardened Repository, Network mode only). Removed as unstated: supported distro list, perl requirement, task-slot sizing (1 core, 2 GB), log line text, HotAdd/PVSCSI and NBDSSL advice, leftover HotAdd disk handling, and the system_requirements source (too thin to confirm).
Method: documentation only; no commands were run.
