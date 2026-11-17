---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-staged-restore
name: veeam-staged-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [staged-restore, veeam-restore, veeam-virtual-lab, gdpr-backups, backup-data-erasure, veeam]
level: advanced
status: draft
description: "Use Veeam Staged Restore to run a script against a VM in a virtual lab before it reaches production: GDPR data removal, credential resets, malware cleanup, and constraints."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam Staged Restore

Staged Restore starts the VM from backup inside an isolated **virtual lab** (SureBackup
infrastructure), runs your script inside it, then migrates the modified VM to production.

## Use cases
- **Privacy**: remove records that were erased in production after the backup (GDPR right to
  erasure) before restoring a VM.
- Security: disable compromised accounts, rotate local passwords, remove known malware/IOCs
  before the VM touches the network.
- Change config (IP addresses, license servers) for the target environment.

## Requirements
- A configured **virtual lab** and an **application group** (for dependencies like a DC if
  the script needs AD).
- Script (PowerShell/batch for Windows, shell for Linux) and guest credentials.
- vSphere (Staged Restore is part of Entire VM restore → "Staged restore" option).

## Steps
1. Entire VM restore → choose restore point and target → enable **Staged restore**.
2. Select virtual lab, application group (optional), script path, credentials, and
   max time allowed for the script.
3. Veeam publishes the VM in the lab (instant recovery style), runs the script via VIX or
   network, then Storage vMotion/quick migration moves it to production storage.
4. Check the session log for script output and exit code.

## Example script (Windows, remove erased records)
```powershell
Invoke-Sqlcmd -ServerInstance localhost -Database crm -Query "DELETE FROM customers WHERE id IN (SELECT id FROM erasure_log)"
exit $LASTEXITCODE
```
Keep the erasure log outside the backup (a separate, current system) so you can replay
deletions on any restore.

## Gotchas
- The VM runs from backup storage during the lab phase: slow repositories make this slow.
- Scripts must be idempotent and non-interactive with a time limit.
- Apps needing external dependencies won't start without the application group.

## Verify
Session log shows script exit 0; restored VM in production lacks the removed data (query
check) and has the applied changes.
