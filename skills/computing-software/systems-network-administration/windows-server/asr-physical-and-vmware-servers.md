---
id: computing-software.systems-network-administration.windows-server.asr-physical-and-vmware-servers
name: asr-physical-and-vmware-servers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-site-recovery, asr, asr-physical-servers, vmware-to-azure, replication-appliance, mobility-service, configuration-server]
level: advanced
status: docs-checked
description: "Replicate physical Windows servers and VMware VMs to Azure with ASR: replication appliance, mobility service push or manual install, process server sizing and failback."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/vmware-azure-architecture-modernized
  - https://learn.microsoft.com/en-us/azure/site-recovery/physical-server-azure-architecture-modernized
  - https://learn.microsoft.com/en-us/azure/site-recovery/replication-appliance-support-matrix
  - https://learn.microsoft.com/en-us/azure/site-recovery/vmware-physical-azure-classic-deprecation
  - https://learn.microsoft.com/en-us/azure/site-recovery/vmware-azure-install-mobility-service
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replicate physical servers and VMware VMs with ASR

## Architecture (modernized)
- **Azure Site Recovery replication appliance** on-premises, registered to the vault. It includes the built-in
  process server. Appliance OS: Windows Server 2022 (existing Windows Server 2019 appliances keep receiving
  updates but cannot be upgraded in place); minimum 8 CPU cores, 16 GB RAM, an 80 GB OS disk and a 620 GB data
  disk; English locale; do not enable AD DS, IIS or Hyper-V roles on it.
- **Mobility service** agent on every protected machine: block-level, near-continuous replication. Crash-consistent
  recovery points every five minutes; app-consistent points every 1 to 12 hours per policy (disabled by default).
  Maximum recovery point retention is 15 days.
- Replication data lands in a cache storage account, then in managed disks in Azure.
- The classic (configuration server) experience is no longer supported: enabling classic replication was blocked on
  31 Jan 2026 and support ended in March 2026. Move machines to the modernized experience.

## Physical servers
1. Deploy the appliance and register it to the vault, then discover or add the machines.
2. Mobility service: automatic push installation is recommended (the process server needs an account with local or
   domain administrator rights on Windows, used only for push install and updates), or install it manually from the
   UI as described in the Mobility service overview.
3. Enable replication: select machines, target resource group, VNet, size, disks, policy.

## Sizing
- An appliance with its built-in process server handles up to 200 machines at the documented top configuration
  (16 vCPUs, 32 GB RAM, 1 TB cache disk, data change rate above 1 TB to 2 TB). Use more appliances beyond that;
  machines can be switched between healthy appliances in the same vault.
- Use the Deployment Planner for VMware estates to size bandwidth and storage.

## Failback
- VMware: re-protect to the original or an alternate VMware VM using a healthy appliance that can reach the datastore.
- Physical: the modernized physical-server architecture page says failback is not supported; confirm current
  behaviour in the documentation before planning on it.

## Verify
- [ ] Replicated items Protected; appliance health green; RPO within policy.

## Checked
Date 2026-10-27. Documentation: modernized VMware and physical architecture pages, replication appliance support
matrix (page dated 15 Oct 2026), classic deprecation page, push-install preparation page. Confirmed: appliance OS and
hardware, role restrictions, recovery point cadence and 15-day maximum, 200-machine sizing row, classic retirement.
Method: documentation only; no commands were run.
