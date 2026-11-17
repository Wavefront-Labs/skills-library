---
id: computing-software.systems-network-administration.windows-server.azure-backup-mars-agent
name: azure-backup-mars-agent
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-server-backup, mars-agent, azure-backup, recovery-services-vault, system-state-backup, passphrase, offline-seeding]
level: practitioner
status: docs-checked
description: "Back up Windows Server files, folders and system state to Azure with the MARS agent: vault, registration, passphrase, schedules, retention and restores."
sources:
  - https://learn.microsoft.com/en-us/azure/backup/backup-windows-with-mars-agent
  - https://learn.microsoft.com/en-us/azure/backup/backup-azure-restore-windows-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Backup MARS agent

Microsoft Azure Recovery Services (MARS) agent backs up files, folders and system state
directly to a Recovery Services vault. 
## Setup
1. Create a Recovery Services vault.
2. Vault > Backup > On-premises > Files and folders / System State > download agent and
   vault credentials.
3. Install agent, register with credentials, set an **encryption passphrase**.
   Store it securely: restoring to another server requires the passphrase.

## Schedule
Set the schedule in the MARS agent console. Up to three backups per day can be scheduled for files and folders.

## Throttling and seeding
- Network bandwidth can be limited for work and non-work hours (Change Properties in the agent).
- Large initial backups: offline seeding with Azure Data Box.

## Restore
- Same server: Recover Data > This server > Files and folders > browse by date, mount as
  a volume, copy files.
- Another server: use the "Another server" option, select the source machine and provide the passphrase.
- System state: restore the files, then apply with `wbadmin start systemstaterecovery`.

## Verify
- [ ] Vault Backup Jobs show a recent success.
- [ ] Restore test to a different server proves the passphrase is correct.

## Checked
2026-10-28: Confirmed on Learn pages backup-windows-with-mars-agent and backup-azure-restore-windows-server: up to three daily backups, work/non-work bandwidth setting, Azure Data Box offline backup, restore to another machine needs the passphrase, `wbadmin start systemstaterecovery` exists. Removed: vault-credential validity period, passphrase length, redundancy-lock claim, MABS/DPM statement, OB* PowerShell schedule block, once-per-day and staging-space system state claims, iSCSI mount detail.
Method: documentation only; no commands were run.
