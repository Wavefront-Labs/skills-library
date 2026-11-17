---
id: computing-software.systems-network-administration.windows-server.asr-azure-to-azure-disaster-recovery
name: asr-azure-to-azure-disaster-recovery
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-site-recovery, azure-to-azure-dr, a2a, recovery-services-vault, failover]
level: advanced
status: docs-checked
description: "Protect Azure VMs running Windows Server with Azure Site Recovery Azure-to-Azure replication: enable, network mapping, test failover, failover and re-protect."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-tutorial-enable-replication
  - https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-tutorial-failover-failback
  - https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-architecture
  - https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-about-networking
  - https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-how-to-reprotect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure-to-Azure disaster recovery with ASR

## Enable
1. Recovery Services vault in the **target** region.
2. VM > Disaster recovery (or vault > Enable replication > Azure): choose target region, target resource group,
   VNet/subnet, availability zone or set, replication policy (recovery point retention, app-consistent snapshot
   frequency). Defaults: retention one day, app-consistent snapshots disabled (zero hours).
3. ASR installs the Site Recovery Mobility service extension on the VM; disk writes land first in a cache storage
   account in the source region, then recovery points are built in the target. Crash-consistent points are created
   every five minutes; app-consistent points only if the policy sets a frequency.
4. Outbound HTTPS 443 from the VM must be allowed (NSG service tags): `Storage.<source-region>`,
   `AzureActiveDirectory`, `EventHub.<target-region>` (monitoring) and `AzureSiteRecovery`; add `AzureKeyVault` for
   ADE VMs enabled from the portal and `GuestAndHybridManagement` for mobility agent auto-upgrade from the portal.
   Target-region rules use `Storage.<target-region>` and `EventHub.<source-region>` for reprotect.

## Network
- Target VNet and subnet are auto-created or chosen; static source IPs are reused on the target if available.
- Domain controllers: for a few apps and one DC, replicate the DC with Site Recovery; for larger estates keep an
  additional DC in the target region. In a test failover do not include all DCs in the test network.

## Test and fail over
```text
Vault > Replicated items > VM > Test failover > recovery point (Latest processed / Latest app-consistent / ...) > isolated test VNet
-> validate -> Cleanup test failover
Vault > Replicated items > VM > Failover -> Commit
```
Recovery point choices for plans: Latest processed (lowest RTO), Latest app-consistent, Latest multi-VM processed,
Latest multi-VM app-consistent; Custom is for single VMs only. Commit deletes the other recovery points.
Use **recovery plans** (up to 100 protected instances) to order tiers and run scripts or runbooks between groups.

## Re-protect and fail back
After failover, **Re-protect** (vault > Replicated items > Re-Protect, direction secondary to primary) seeds the
original region with the latest data, then replicates deltas; fail back once it is replicating. The target VNet
cannot be changed during reprotect (redo network mapping), and the resource group cannot change when reprotecting
to the original VM.

## Gotchas
- Multi-VM consistency groups give shared recovery points but affect workload performance; use only where needed.
- ADE and CMK VMs need key vault access for the keys and secrets that ASR copies to the target region.
- A disk added later shows a warning on the replicated VM until you enable replication for it (managed disks).
- Availability type (single, set, zone) of the target cannot be changed in place: disable and re-enable replication.

## Verify
- [ ] Test failover runs quarterly with the app validated in the isolated VNet; RPO in the replicated item health.

## Checked
Date 2026-10-27. Documentation: Site Recovery Azure-to-Azure architecture, networking (service tags), reprotect,
test failover, failover and recovery plan overview, Active Directory guidance and common questions pages.
Confirmed: service tags, policy defaults, recovery point options, five-minute crash-consistent points, reprotect
limits, 100 instances per plan, new-disk warning.
Method: documentation only; no commands were run.
