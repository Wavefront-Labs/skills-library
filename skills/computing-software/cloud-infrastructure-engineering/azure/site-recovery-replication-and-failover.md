---
id: computing-software.cloud-infrastructure-engineering.azure.site-recovery-replication-and-failover
name: site-recovery-replication-and-failover
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, site-recovery, asr, disaster-recovery, replication, recovery-plan, test-failover, failover, failback, re-protect, azure-to-azure, zone-to-zone, vmware-to-azure, hyper-v-to-azure, physical-to-azure, replication-appliance, mobility-service, recovery-points, crash-consistent, app-consistent, rpo-alerts, network-mapping, target-network, recovery-services-vault, dr-drill]
level: advanced
status: docs-checked
description: "Set up Azure Site Recovery for Azure VMs: replication policy, cache account, recovery plans, isolated test failover, recovery point choices and Log Analytics monitoring."
sources: ["https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-architecture", "https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-common-questions", "https://learn.microsoft.com/en-us/azure/site-recovery/azure-to-azure-support-matrix", "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-test-failover-to-azure", "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-runbook-automation", "https://learn.microsoft.com/en-us/azure/site-recovery/monitor-log-analytics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Site Recovery — replicate, rehearse, fail over, come back

**Goal:** VM-based workloads that can be brought up in another region (or zone) in
the order the application needs, within the RTO you promised, by someone following a
runbook — proven by a drill that touched no production traffic.

## 1. Scope
Azure VM to another region, or zone to zone, using the Mobility service extension and a
**cache storage account in the source region**. Site Recovery is the VM tier only: PaaS and
databases with their own replication (SQL AG, Cosmos, PostgreSQL read replicas) use their
own geo features. VMware, physical and Hyper-V scenarios use different components; follow
the Site Recovery docs for those.
Site Recovery creates a crash-consistent recovery point every five minutes (not changeable);
app-consistent snapshots follow the frequency in the replication policy. RTO depends on
boot time plus recovery plan scripts: measure it in a drill.

## 2. Enable Azure-to-Azure
The vault is a Recovery Services vault in the TARGET region. Portal or PowerShell is the
practical path. Key choices:
- source VMs, target resource group, target VNet/subnet, cache storage account (source region);
- replication policy: the default retains recovery points for one day with app-consistent
  snapshots disabled (frequency 0 hours); retention goes up to 15 days with managed disks;
- availability: target zone or availability set; a capacity reservation group in the target
  can be attached to guarantee capacity (see the capacity reservation docs).
- Normal churn supports up to 54 MB/s per VM; eligible High Churn configurations support up
  to 500 MB/s per VM and 250 MB/s per disk, others stay at 54 or 100 MB/s. Check the support
  matrix for your disk and VM size before promising DR for write-heavy databases.
- **Network mapping** maps source VNet to target VNet; public IPs, NSGs and load balancer
  membership are set in each VM's target Compute and Network settings or in the recovery plan.
- Trusted Launch, Ultra disks, shared disks and some sizes have specific support; check the
  support matrix and the common-questions page before enabling.
- Mobility extension names begin `Microsoft.Azure.RecoveryServices.SiteRecovery.` (troubleshooting page).

## 3. Recovery plans
A **recovery plan** has ordered **groups** of VMs (new plans start with every VM in Group 1)
with pre and post actions: Azure Automation runbooks and manual actions. A runbook receives
a `RecoveryPlanContext` (see the runbook automation page). Keep one plan per application boundary and version-control the runbooks.

## 4. Drill, fail over, fail back
- **Test failover**: pick a recovery point and a network isolated from the production
  recovery network; validate; *Cleanup test failover* deletes the test VMs. Time to green is your real RTO.
- **Recovery point options**: Latest processed (low RTO), Latest app-consistent, multi-VM
  variants for VMs with multi-VM consistency, and Custom (a single VM, not via a plan).
- **Failover** then commit, and update DNS/edge routing; script the cut-over.
- **Re-protect** reverses replication; **failback** is a failover in the other direction.
  Read the failover and re-protect pages before a real event; this skill did not verify their timings.

## 5. Monitor
- Vault Replicated items: replication health, current RPO, latest recovery points.
- Diagnostic settings send `AzureSiteRecoveryJobs`, `AzureSiteRecoveryEvents`,
  `AzureSiteRecoveryReplicatedItems` and replication-stats categories to Log Analytics; the
  monitoring page's sample query buckets `rpoInSeconds_d` (<=900 s is "<15Min").

## Gotchas
- Target capacity is not reserved by default; use a capacity reservation group for Tier-0 workloads.
- The cache storage account must be reachable from the VM; blocked access stalls replication.
- Failover does not update application config; connection strings to source-region services must be flipped by scripts.
- App-consistent snapshots on Windows use VSS; Storage Spaces Direct and Scale-Out File Server support crash-consistent points only.

## Verify
- [ ] Tier-0/1 VMs show healthy replication and current RPO within target.
- [ ] Test failover of the recovery plan into the isolated network completed within the last quarter; RTO recorded; cleanup done.
- [ ] DNS/edge cut-over steps scripted in the plan's runbooks and rehearsed.

## Checked
2026-10-28. Confirmed against the Azure-to-Azure architecture, common questions, support
matrix, test failover, runbook automation and Log Analytics monitoring pages: five-minute
crash-consistent points, default policy (one day, app-consistent disabled), 15-day maximum
with managed disks, churn limits, recovery point options, `RecoveryPlanContext`, log
categories, isolated test network, S2D and SOFS limitation. Removed as unconfirmed: the
typical RTO and RPO ranges, per-disk cache churn figures, retention bounds in hours,
recovery plan size cap, VMware and Hyper-V rows, re-protect timings, 100-VM cap, the
Business Continuity Center and RecoveryPoints table names, `az backup vault create` example.
Method: documentation only; no commands were run.
