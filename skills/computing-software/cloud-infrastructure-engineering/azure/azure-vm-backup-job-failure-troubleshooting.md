---
id: computing-software.cloud-infrastructure-engineering.azure.azure-vm-backup-job-failure-troubleshooting
name: azure-vm-backup-job-failure-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-backup, backup-errors, vm-backup, vss]
level: advanced
status: docs-checked
description: "Troubleshoot Azure VM backup failures from the error code: VSS writer and service errors, snapshot limits, policy blocks, antivirus, network timeouts and premium storage quota."
sources: ["https://learn.microsoft.com/azure/backup/backup-azure-vms-troubleshoot", "https://learn.microsoft.com/azure/backup/backup-azure-vms-introduction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM backup job failure troubleshooting

**Goal:** get a failing VM backup green again from its error code.

## Find the error
```bash
az backup job list -g rg -v vault1 --status Failed -o table
```
Or Backup center -> Backup jobs -> filter Failed, then open the job to read the error code and message. Look the code up on the "Troubleshoot Azure VM backup" page.

## Common codes (from the Microsoft troubleshooting page)
| Error code | Cause | Fix |
|---|---|---|
| `ExtensionFailedVssWriterInBadState` | VSS writers in a bad state | Run `vssadmin list writers` from an elevated prompt; restart the service of every writer whose state is not `[1] Stable`; the page lists further steps if that fails (including a limited-IOPS cause) |
| `ExtensionFailedVssServiceInBadState` | VSS service in a bad state | Restart the Volume Shadow Copy service (`net stop VSS`, then start it) and retry |
| `ExtensionFailedSnapshotLimitReachedError` | Snapshot limit exceeded on some attached disks | Delete unneeded disk blob snapshots (only snapshot blobs, never the disk blobs); if soft-delete is enabled on the disk storage accounts, adjust retention so snapshots stay under the maximum |
| `UserErrorRequestDisallowedByPolicy` | An Azure Policy (for example a Deny on tags) blocks the snapshot operation | Change the policy effect from Deny to Modify, or create the backup resource group manually using the naming schema Azure Backup requires |
| `ExtensionFailedTimeoutVMNetworkUnresponsive` | Network calls delayed during the snapshot | Step 1 on the page: set the `SnapshotMethod` / `CalculateSnapshotTimeFromHost` registry values under `HKLM\SOFTWARE\Microsoft\BcdrAgentPersistentKeys` to take the snapshot through the host first; further steps on the page |
| `ExtensionSnapshotFailedNoSecureNetwork` | Failure to create a secure channel | Add `SchUseStrongCrypto` = 1 (dword) for each .NET Framework version in the registry, as the page describes |
| `UserErrorBCMPremiumStorageQuotaError` | Not enough free space in the storage account to copy the snapshot (premium VMs on VM backup stack V1) | Allocate only 50 percent (17.5 TB) of the storage account space so the snapshot copy can complete |
| `UserErrorUnableToOpenMount` | Backup extension cannot open the VM's mount points | Make sure all mount points are accessible |
| `VMRestorePointInternalError` with `IaaSBcdrExtension.exe` faulting in Event Viewer | Antivirus blocks the backup extension | Exclude the `Packages\Plugins\Microsoft.Azure.RecoveryServices.VMSnapshot` and `WindowsAzure\Logs\Plugins\Microsoft.Azure.RecoveryServices.VMSnapshot` directories on the system drive |
| `380008` / `AzureVmOffline` | Recovery Services extension cannot install because the VM is not running | Start the VM and retry |

## General
- To rule out snapshot extension problems, uninstall the extensions to force a reload, then retry the backup.

## Verify
- [ ] `az backup protection backup-now -g rg -v vault1 -c <container> -i <item> --retain-until <DD-MM-YYYY>` completes and the job shows `Completed`.

## Checked
Date: 2026-10-31. Confirmed against "Troubleshoot Azure VM backup" (backup-azure-vms-troubleshoot): every error code, cause and fix in the table above, including the antivirus paths and the 50 percent / 17.5 TB guidance. CLI flags were checked against the az backup reference by the batch tooling.
Removed as unconfirmed or wrong: the guest-agent and 168.63.129.16 rows, `UserErrorVmProvisioningStateFailed`, `UserErrorKeyvaultPermissionsNotConfigured`, `ExtensionOperationFailedForManagedDisks`, `BCMV2VMSnapshotFailed`, the `USEVSSCOPYBACKUP` advice, the `AzureBackupRG_<region>_1` lock claim (the documented cause of `UserErrorRequestDisallowedByPolicy` is an Azure Policy, not a lock), the Linux pre/post script and log paths, and the jmespath query and `AddonAzureBackupJobs` table name. The source link to the troubleshoot-vm-backup-fails-snapshot-timeout page was dropped because it returned 404.
Method: documentation only; no commands were run.
