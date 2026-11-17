---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-gateway-and-mount-servers
name: veeam-gateway-and-mount-servers
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-gateway-server, veeam-mount-server, backup-repository, smb-repository, file-level-restore]
level: advanced
status: docs-checked
description: "Place Veeam gateway servers for SMB/NFS/dedupe-appliance repositories and mount servers for file-level and instant recovery, and fix slow restores caused by bad placement."
sources:
  - https://helpcenter.veeam.com/docs/vbr/userguide/gateway_server.html
  - https://helpcenter.veeam.com/docs/vbr/userguide/mount_server.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam gateway and mount servers

## Gateway server
A gateway server "bridges" the backup server and the backup repository. It is required for shared folder repositories, Dell Data Domain, HPE StoreOnce and object storage repositories, because these cannot host Veeam Data Movers. The gateway hosts the target Data Mover.
- The gateway can be a Windows or Linux machine, or a Hyper-V host (not for deduplicating appliances), added as a managed server. ReFS fast clone needs a Windows gateway. Dedupe appliances over Fibre Channel need at least one explicitly selected gateway.
- Explicit selection: the gateways must sit as close to the repository as possible. Exception: with a dedupe appliance using source-side deduplication, put gateways closer to the proxy to cut network traffic.
- If you select only one gateway explicitly and it is not accessible, the job fails. Veeam distributes tasks over available gateways by connectivity and load; if connection to a gateway is lost mid-job the job fails, and a new gateway is chosen at the next start.
- Automatic selection: for a VMware backup job the gateway is the proxy assigned first to process the workload, so check where that proxy sits relative to the share. Synthetic operations run on the repository's mount server (failing over to the backup server).
- For an NFS repository with the Veeam Software Appliance as gateway, the NFS export must be set to `all_squash`.

## Mount server
Required for guest OS file restore, application item restore, secure restore, Scan Backup, Instant Recovery, Instant Disk Recovery, instant file share recovery and restore of objects from file or object storage backups.
- Mount servers are created per repository: a Windows mount server (any 64-bit Windows machine in the infrastructure) and a Linux mount server (RHEL/Rocky-based). Every repository needs at least one; for scale-out repositories, set it for each extent.
- Keep the mount server in the same site as the repository, otherwise data travels across the network between sites. With several sites, configure at least one per site.
- If none is set or it is unavailable, Veeam fails over to the default mount servers (on a Windows backup server, the backup server itself).
- Enabling the vPower NFS Service on the mount server is recommended; it lets VMs run directly from backup files.
- Linux mount servers need `libmsi1` and `ntfs-3g`. The Veeam Software Appliance and Veeam Infrastructure Appliance do not support third-party software, so use another Linux machine if you need antivirus scan for secure restore.
- A Windows mount server is required for, among others: VMware replication with Re-IP rules, application item restore, Instant Disk Recovery of Windows workloads, and Instant Recovery of Windows workloads from another platform.
- The mount server must reach the repository and the original VM.

## Troubleshooting
Slow file-level restore from a remote repository: check the repository's mount server setting first.

## Verify
Check the repository's mount server and gateway settings, and run a guest file restore to confirm the data stays in one site.

## Checked
2026-11-09. Read in full: Veeam Help Center "Gateway Servers" and "Mount Servers" (build 13.1.2.57). Removed as unstated: firewall ports, vPower write cache sizing, SMB permissions, gateway task-slot sizing, 10 GbE advice, error-message strings and session-log text. The bp.veeam.com landing source was dropped (not read in detail).
Method: documentation only; no commands were run.
