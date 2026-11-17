---
id: computing-software.cloud-infrastructure-engineering.azure.site-recovery-replication-errors-and-mobility-service
name: site-recovery-replication-errors-and-mobility-service
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, site-recovery, asr-troubleshooting, mobility-agent-errors, replication-health, rpo]
level: advanced
status: docs-checked
description: "Troubleshoot Azure Site Recovery replication: Mobility service install and upgrade errors, high churn and RPO breaches, outbound connectivity and initial replication stalls."
sources: ["https://learn.microsoft.com/azure/site-recovery/azure-to-azure-troubleshoot-errors", "https://learn.microsoft.com/azure/site-recovery/azure-to-azure-troubleshoot-network-connectivity", "https://learn.microsoft.com/azure/site-recovery/site-recovery-azure-to-azure-troubleshoot-replication", "https://learn.microsoft.com/azure/site-recovery/vmware-physical-mobility-service-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site Recovery replication and Mobility service troubleshooting

**Goal:** get unhealthy replicated items back to healthy with RPO in bounds.

## Where to look
- Vault → Replicated items → item → **Error details** (code + recommendation); Site Recovery jobs.
- If vault diagnostics go to Log Analytics, query the Site Recovery tables there (inspect the schema first).

## Common issues
| Symptom / code | Cause | Fix |
|---|---|---|
| Outbound connectivity errors, enable replication fails | VM cannot reach Site Recovery and storage endpoints | Allow service tags `AzureSiteRecovery`, `Storage.<region>`, `AzureActiveDirectory`, `EventHub.<region>` in the NSG (outbound 443), or proxy settings |
| Mobility extension install fails | VM agent unhealthy, unsupported OS/kernel | Fix guest agent, check supported kernel list for Linux, update OS |
| RPO critical / high churn | Disk write rate exceeds per-disk/VM limits (churn) | Check the data change rate per disk; exclude temp/paging disks; split workload |
| Initial replication stuck at 0% | Snapshot or network issue, very large disks | Check job, bandwidth, retry; for VMware check process server health |
| App-consistent points missing | VSS failures in guest | Fix VSS writers; Linux needs pre/post scripts |
| Mobility agent upgrade pending | Auto-update disabled or automation account issue | Check the Mobility agent update settings and the automation account |

## VMware/physical (modernized)
- Mobility service talks to the **replication appliance**; check appliance health (process server, push installer).
- Find the Mobility service log locations and push-install prerequisites in the Site Recovery VMware troubleshooting docs (not confirmed here).

## Verify
- [ ] Item shows Replication health Healthy, RPO under threshold for 24 h, recent app-consistent point.

## Checked

2026-10-28. Confirmed on the Site Recovery Azure-to-Azure network connectivity troubleshooting page: outbound HTTPS 443 NSG rules for service tags Storage.<region>, AzureActiveDirectory, EventHub.<region> and AzureSiteRecovery. Removed: the GuestAndHybridManagement tag, Log Analytics table and category names, the KQL query, Mobility log paths, push install prerequisites and the update-setting label (not found in fetched pages). Troubleshooting table rows are general guidance.

Method: documentation only; no commands were run.
