---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cluster-name-object-ad-permissions
name: hyper-v-cluster-name-object-ad-permissions
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [cluster-name-object, cno, failover-cluster, active-directory, hyper-v]
level: advanced
status: docs-checked
description: "Manage the failover cluster name object in Active Directory: prestaging, OU permissions for VCOs, repairing passwords and recovering a deleted CNO."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/prestage-cluster-adds
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-cluster-accounts-overview
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/high-availability/troubleshoot-issues-accounts-used-failover-clusters
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Cluster name object and AD permissions

**Goal:** the cluster's AD computer account (CNO) works, and it can create computer objects for clustered roles.

## Roles of the accounts
- **CNO**: the cluster name's computer account, created with the cluster. If you give a NetBIOS name it is created beside the node computer objects.
- **VCOs**: computer accounts for clustered roles with a client access point. They are created in the CNO's OU, so the CNO needs *Create Computer objects* there.

## Prestage when admins lack OU rights
1. Create computer account `HVCL01` in the target OU and **disable** it (the creation process uses this to confirm the name is not in use).
2. Grant the installing user *Full Control* on it.
3. Run `New-Cluster -Name HVCL01 ...`.
4. Grant the CNO *Create Computer objects* on the OU, or prestage VCOs for each clustered role.

If the CNO sits in the default Computers container, a cluster admin can create up to 10 VCOs without extra configuration; more needs the CNO to be granted Create Computer objects on that container.

## Common problems
| Event or symptom | Cause | Fix |
|---|---|---|
| 1193, 1194, 1206, 1207 | CNO or VCO deleted, changed or missing permissions | Restore the account or permissions, then repair the object |
| Role network name fails and the domain quota is reached | Domain-wide quota for creating computer objects (default 10) | Prestage, or raise `ms-DS-MachineAccountQuota` only after reviewing |
| Password problems with the CNO | Account password reset or changed | Failover Cluster Manager: Cluster Core Resources, take the Name resource offline, then *More Actions*, **Repair Active Directory Object** (greyed out unless the Name resource is offline) |

Give cluster administrators the **Reset password** permission on the CNO ahead of time.

## Verify
`Get-ADComputer HVCL01 -Properties Enabled,PasswordLastSet` shows the account enabled; a new clustered role comes online with its network name.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the prestage page: the disabled prestaged CNO, Full Control for the installing user, Create Computer objects for the CNO on the OU, and the 10-VCO allowance in the default Computers container. Confirmed in the accounts overview and troubleshooting pages: events 1193, 1194, 1206 and 1207 indicate account or permission problems, the domain-wide default quota of 10 (ms-DS-MachineAccountQuota), the Reset password permission, and that Repair Active Directory Object is greyed out unless the cluster Name resource is offline. Removed as unconfirmed: event 1196 and its DNS cause, the AD Recycle Bin recovery row, and the stale-account cleanup advice.

Method: documentation only; no commands were run.
