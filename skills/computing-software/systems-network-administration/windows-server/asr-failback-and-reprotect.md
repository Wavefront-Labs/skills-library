---
id: computing-software.systems-network-administration.windows-server.asr-failback-and-reprotect
name: asr-failback-and-reprotect
category: computing-software
field: systems-network-administration
product: windows-server
tags: [azure-site-recovery, asr-failback, reprotect, asr-hyper-v, disaster-recovery]
level: advanced
status: docs-checked
description: "Complete the Azure Site Recovery cycle after a failover: commit, reprotect from Azure back to on-premises, planned failback, and re-enable replication."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/hyper-v-azure-failback
  - https://learn.microsoft.com/en-us/azure/site-recovery/failover-failback-overview-modernized
  - https://learn.microsoft.com/en-us/azure/site-recovery/concepts-types-of-failback
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-failover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASR failback and reprotect

Failover to Azure is only half of DR. Coming back without losing changes made in Azure is the other half.

## After a failover
1. **Commit** the failover once the Azure VMs are confirmed good. Until commit you can change the recovery point;
   commit deletes all the recovery points held by the service and the change option disappears.
2. Run the workload in Azure.

## Hyper-V to Azure failback
Prerequisites: Azure VMs use managed disks; the on-premises Hyper-V host (or VMM server) is running and connected
to Azure; failover and commit are complete. No Site Recovery components are needed for Hyper-V failback. For VMM,
the VM metadata must still exist in the VMM database or failback fails.
1. Vault > Replicated items > VM > **Planned failover** (for a plan: Failover > Planned Failover); direction Azure to
   on-premises. Planned failback turns the Azure VM off and downloads the latest changes, so no data loss is expected.
   - **Synchronize data before failover (synchronize delta changes only)**: minimises downtime because the Azure VM
     keeps running during the sync.
   - **Synchronize data during failover only (full download)**: faster when most of the disk has changed, because
     no checksums are calculated.
2. Alternate location only: choose **Create on-premises virtual machine if it does not exist**, with a virtual
   switch of the same name as on the original server. Alternate-location failback is not possible with recovery plans.
3. The VM goes to commit pending: select **Commit** (for alternate location this deletes the Azure VM and disks),
   then **Reverse Replicate** to protect the on-premises VM to Azure again (only deltas replicate).
Do not cancel the failback job during data synchronization: the on-premises VM can be left unbootable until the
failover is rerun.

## VMware and physical (modernized)
1. Ensure a healthy replication appliance is registered to the vault; select it for reprotect. It needs access to
   the datastore of the source machine; no separate Azure process server or Linux scale-out master target is needed.
2. **Re-protect** the Azure VM to on-premises: only disks originally replicated to Azure replicate back; disks added
   in Azure do not. The on-premises VM is turned off during reprotect.
3. **Planned failover** to on-premises (choose a crash-consistent point), commit, then re-protect again to Azure.
4. Storage vMotion of replicated items is not supported. The modernized architecture page states failback is not
   supported for physical servers; the older failback concepts page says a physical machine can only fail back as a
   VMware VM. Confirm in the current documentation before relying on physical failback.

## Gotchas
- Failback needs connectivity (VPN/ExpressRoute) sized for the delta; a long Azure run means large deltas.
- Azure-only agents and extensions installed while running in Azure stay in the VM; remove them if unwanted.

## Verify
- [ ] On-premises VM running with Azure-period data; replication to Azure healthy again; runbook timings recorded.

## Checked
Date 2026-10-27. Documentation: Hyper-V failback, failover/failback overview (modernized), types of failback, failover
and physical-server architecture pages. Confirmed: sync option semantics, alternate-location and plan limits, commit
behaviour, appliance-based reprotect, replicated-disk rule. The physical failback statement is flagged as
inconsistent between pages, so no claim is made beyond naming both.
Method: documentation only; no commands were run.
