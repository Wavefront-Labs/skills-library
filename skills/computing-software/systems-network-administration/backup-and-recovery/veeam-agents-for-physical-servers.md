---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-agents-for-physical-servers
name: veeam-agents-for-physical-servers
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam-agent, veeam, physical-server-backup, protection-group, veeamconfig, blksnap, bare-metal-recovery]
level: practitioner
status: draft
description: "Protect physical Windows and Linux servers with Veeam Agents: managed protection groups and policies, backup modes, Linux snapshot module and veeamconfig, and recovery media."
sources:
  - https://helpcenter.veeam.com/docs/backup/agents/introduction.html
  - https://helpcenter.veeam.com/docs/agentforlinux/userguide/overview.html
  - https://helpcenter.veeam.com/docs/agentforwindows/userguide/overview.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Veeam Agents for physical servers

**Goal:** back up physical servers, cloud VMs and unsupported hypervisor guests into the same repositories as VM backups.

## Managed mode (recommended)
From the backup server: Inventory > Physical Infrastructure > **Protection group** (by AD container, list of computers, CSV, or pre-installed agents). Veeam deploys agents and applies **backup policies**:
- **Server** type for servers (managed by backup server, supports failover clusters via "Failover cluster" mode).
- **Workstation** type for laptops (backup on schedule or when connected, tolerant of being offline).

## Backup modes
- **Entire computer**: all volumes; enables bare-metal and volume restore. Default for servers.
- **Volume level**: selected volumes.
- **File level**: selected folders/files; slower, for data-only protection.
Application-aware processing for SQL, Exchange, Oracle on Windows; pre/post scripts on Linux.

## Linux specifics
- Snapshots via the Veeam kernel module (`veeamsnap`, or `blksnap` in newer releases); built with DKMS for your kernel. Kernel upgrades need the module rebuilt; Secure Boot requires signing (or the distro's packaged signed module).
- CLI:
```bash
veeamconfig job list
veeamconfig job start --name 'BackupJob1'
veeamconfig session list
veeamconfig session log --id <session-id>
```
- Non-snapshot mode exists (for unsupported kernels) but backs up live, possibly inconsistent files.

## Recovery
- Create **recovery media** (bootable ISO/USB with drivers) per hardware model; test boot it.
- Bare-metal restore from the recovery media to same or different hardware; volume and file restores from the console or the agent.
- Instant recovery of agent backups to a VM (vSphere/Hyper-V) is also possible for fast RTO.

## Gotchas
- Agents count against licences per server/workstation.
- Kernel updates without module rebuild silently switch Linux agents to failing jobs; alert on job failures after patch nights.

## Verify
Job sessions succeed for every protected machine, and a periodic bare-metal or instant-to-VM restore boots successfully.
