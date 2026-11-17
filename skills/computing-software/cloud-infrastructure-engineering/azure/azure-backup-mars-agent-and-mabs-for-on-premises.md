---
id: computing-software.cloud-infrastructure-engineering.azure.azure-backup-mars-agent-and-mabs-for-on-premises
name: azure-backup-mars-agent-and-mabs-for-on-premises
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-backup, mars-agent, mabs, azure-backup-server, dpm, recovery-services-vault, on-premises-backup, files-and-folders, system-state, passphrase, offline-seeding, bandwidth-throttling]
level: practitioner
status: docs-checked
description: "Back up on-prem Windows servers to a Recovery Services vault with the MARS agent (files, folders, system state) or MABS/DPM for workloads, with passphrase and restores."
sources: ["https://learn.microsoft.com/en-us/azure/backup/backup-azure-about-mars", "https://learn.microsoft.com/en-us/azure/backup/install-mars-agent", "https://learn.microsoft.com/en-us/azure/backup/backup-azure-microsoft-azure-backup", "https://learn.microsoft.com/en-us/azure/backup/backup-support-matrix-mars-agent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MARS agent and MABS — on-prem backup into Azure

**Goal:** offsite, immutable-capable backups of on-prem Windows servers without a tape or
second datacentre, restored on demand.

## 1. Choose
| Need | Tool |
|---|---|
| Files, folders, volumes and System State of a Windows machine | **MARS agent** (Microsoft Azure Recovery Services) direct to the vault |
| Workload-aware backup (SQL, Exchange, SharePoint, VMs) with a local disk tier for fast restore | **MABS** (Azure Backup Server) or System Center **DPM**, which use the MARS agent to ship to Azure |

## 2. MARS install and register
1. Vault (Recovery Services, same or nearest region; set storage redundancy before first backup)
   → *Backup* → *On-premises* → *Files and folders* → download agent and **vault credentials**.
2. Install `MARSAgentInstaller.exe` (`MARSAgentInstaller.exe /q` for a silent install; `/?` lists options).
3. Register with the vault credentials; set the **encryption passphrase** (MABS docs: at least 16 characters) and save
   it to Key Vault (the vault can save it there for you) — **Microsoft cannot recover it; lose it and backups are unrestorable**.
4. Schedule (PowerShell module `MSOnlineBackup`):
```powershell
$pol = New-OBPolicy
Add-OBFileSpec -Policy $pol -FileSpec (New-OBFileSpec -FileSpec "<DATA_VOLUME>\Data","<SHARES_VOLUME>\Shares")
Set-OBSchedule -Policy $pol -Schedule (New-OBSchedule -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -TimesOfDay 21:00)
Set-OBRetentionPolicy -Policy $pol -RetentionPolicy (New-OBRetentionPolicy -RetentionDays 30)
# Throttling and proxy are set with Set-OBMachineSetting (see the PowerShell automation page for its switches)
Set-OBPolicy -Policy $pol -Confirm:$false
Start-OBBackup -Policy (Get-OBPolicy)        # first backup now
```
- System State: `Add-OBSystemState`; it stages via Windows Server Backup locally first (needs free space).
- Cache folder: free space of at least 5 to 10 percent of the backup data size, on a local, online volume.
- Large initial seeds: **offline backup** (offline seeding with Azure Data Box); it cannot be used for system state.

## 3. MABS outline
- Dedicated Windows Server with a local SQL Server instance (a remote SQL instance is not supported), a **local storage pool** for short-term disk recovery points, and online
  protection to the vault for long-term. Scratch space must be at least 5% of the data backed up to the cloud.
- MABS v4 runs on Windows Server 2022 and 2019 and supports SQL Server 2022 and 2019; upgrade to v4 only from v3.

## 4. Restore
- MARS: restore files and folders to the same or an alternate machine, and system state to the same machine or, as a System State file, to an alternate machine. Keep the passphrase handy.
- MABS: restore from an online or disk recovery point to the original or an alternate location.

## Gotchas

## Verify
- [ ] The vault lists the server's backup item with a recent completed backup.
- [ ] Passphrase stored in Key Vault; a test restore to another server using it succeeds.

## Checked
2026-10-28. Confirmed on Microsoft Learn (About MARS, Install MARS agent, MARS support matrix, MABS install, PowerShell automation pages): MARS scope and restore options, `MARSAgentInstaller.exe /q`, OB cmdlets used in the sample and `MSOnlineBackup`, 5 to 10 percent cache free space, 16-character minimum passphrase, passphrase unrecoverable and Key Vault save, offline seeding unsupported for system state, MABS v4 platform and SQL support, local SQL only, 5% scratch space. Removed: backups-per-day and 10-day credential figures, bandwidth throttling parameters, Linux and soft-delete claims, firewall and alerting notes.
Method: documentation only; no commands were run.
