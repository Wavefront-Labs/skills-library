---
id: computing-software.systems-network-administration.windows-server.asr-protect-hyper-v-vms
name: asr-protect-hyper-v-vms
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-site-recovery, asr, asr-hyper-v, recovery-services-vault, hyper-v-replica, disaster-recovery, replication-policy]
level: advanced
status: docs-checked
description: "Protect on-premises Hyper-V VMs to Azure with Azure Site Recovery: vault, provider and agent install, replication policy, enable replication and target settings."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/hyper-v-azure-tutorial
  - https://learn.microsoft.com/en-us/azure/site-recovery/hyper-v-azure-support-matrix
  - https://learn.microsoft.com/en-us/azure/site-recovery/hyper-v-azure-common-questions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protect Hyper-V VMs to Azure with ASR

## Prepare Azure
- Recovery Services vault and a target VNet/subnets (plus an isolated test VNet). Replicate to managed disks:
  unmanaged-disk storage accounts were scheduled for full retirement on 30 Sep 2025.

## Prepare Hyper-V
- Hosts: Windows Server 2025, 2022, 2019, 2016 or 2012 R2 with latest updates (Server Core supported); with VMM:
  VMM 2025, 2022, 2019, 2016 or 2012 R2 (VMM 2022 on Server Core is not supported). .NET Framework 4.6.2 or higher on
  the server. Outbound HTTPS 443 to the Azure URLs.
- Do not configure Azure Backup and Site Recovery on the same Hyper-V host: unsupported, can break replication.
- Without VMM: vault > Site Recovery > Prepare infrastructure > Hyper-V site, download the **Azure Site Recovery
  Provider** and vault registration key; install the provider on each host (it works with the Microsoft Azure
  Recovery Services agent) and register to the site.
- With VMM: install the provider on the VMM server; the Recovery Services agent goes on the hosts.

## Replication policy
Tutorial example: copy frequency 5 minutes, recovery point retention 2 hours, app-consistent snapshot frequency 1
hour, initial replication immediately. Copy frequency can be 30 seconds (not for premium storage) or 5 minutes.
Create and associate the policy with the Hyper-V site. Striped volumes and dynamic disks do not support
app-consistent snapshots: set that frequency to zero for such VMs.

## Enable replication
Per VM: target resource group, VNet/subnet, VM size, disk type and which disks to replicate. Guest OS must be
supported for Azure; Generation 2 VMs recover as Generation 2 and need a Gen 2-capable Azure size. OS disk limits: up
to 2 TB for Gen 1, 4,095 GiB for Gen 2 (provider later than 2.0.9214.0 for large OS disks, managed disks only).
PowerShell: `New-AzRecoveryServicesAsrReplicationProtectedItem -HyperVToAzure ...`.

## Monitor
Vault > Replicated items: replication health, RPO, last recovery point; email notifications and Azure Monitor alerts
(see asr-replication-health-and-alerts).

## Gotchas
- Shared VHD and shared cluster disks are not supported; Windows Server 2016 Nano Server is not supported.
- Initial replication of large VMs can take long; plan bandwidth.

## Verify
- [ ] Replicated items show Protected, RPO within policy; a test failover done.

## Checked
Date 2026-10-27. Documentation: Hyper-V to Azure support matrix, tutorial and common questions, Az.RecoveryServices
New-AzRecoveryServicesAsrReplicationProtectedItem reference, Hyper-V failback prerequisites (managed disks).
Confirmed: supported host and VMM versions, .NET minimum, provider and agent roles, policy example values, 30 s/5 min
frequency, disk limits, unsupported disk types.
Method: documentation only; no commands were run.
