---
id: computing-software.cloud-infrastructure-engineering.azure.site-recovery-deployment-planner-and-capacity
name: site-recovery-deployment-planner-and-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, site-recovery, deployment-planner, asr-capacity, bandwidth-planning, churn]
level: advanced
status: docs-checked
description: "Use the Site Recovery Deployment Planner to profile VMware VMs and size bandwidth, storage and servers before enabling replication at scale."
sources: ["https://learn.microsoft.com/azure/site-recovery/site-recovery-deployment-planner", "https://learn.microsoft.com/azure/site-recovery/site-recovery-plan-capacity-vmware"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site Recovery Deployment Planner and capacity

**Goal:** know bandwidth, storage, server count and cost before onboarding many machines.

## Scope
- The tool is a command-line tool, executable `ASRDeploymentPlanner.exe` in the parent folder of the downloaded zip. The page says the current version supports only the VMware to Azure scenario; its support matrix also lists Hyper-V to Azure and says Azure to Azure is not supported.
- It profiles remotely with no production impact and needs no Site Recovery components on-premises. Supported vCenter versions listed: 8.0, 7.0, 6.7, 6.5. One run profiles VMs of a single vCenter or ESXi server.
- It profiles only VMs with VMDK and RDM disks, not iSCSI or NFS disks (it uses vCenter performance counters, not guest visibility).
- It does not support OfferID MS-AZR-0017P.

## Prerequisites (profiling and throughput server)
- Windows Server 2016 or 2012 R2, ideally sized like the configuration server; page lists 8 vCPU, 16 GB RAM, 300 GB HDD, .NET Framework 4.5, Visual C++ Redistributable 2012, Azure storage account, administrator access.
- At least 100 GB free disk (for 1,000 VMs, three disks each, 30 days of profiling).
- vCenter statistics level 1 or higher; vCenter port (default 443) open; read-only vCenter account is enough.
- Internet access to `*.blob.core.windows.net` on 443 is optional: you can supply available bandwidth manually at report generation.
- Report generation needs Excel 2013 or later.
- Run from the same hardware class as the configuration server (or from it, if deployed) so reported throughput matches what replication can achieve; from any other server the throughput measured is from that server to Azure.

## What the report covers
- VM eligibility (disk count and size, IOPS, churn, EFI/BIOS boot, OS version).
- Bandwidth needed for delta replication, achievable throughput, VM batching for initial replication, achievable RPO for a given bandwidth.
- Standard or premium storage per VM, number of storage accounts (including cache accounts), Azure core count needed for test failover or failover, recommended Azure VM size.
- Number of configuration servers and process servers to deploy.
- Estimated DR cost (compute, storage, network, licence) with per-VM detail.
- Calculations assume 30 percent workload growth and use the 95th percentile of profiled metrics; both are configurable.

## Upgrading the tool
- If profiling is running and the new version has no profiling fix, keep profiling. If it has a fix, stop and restart profiling on the new version.
- Pass the same output directory when restarting so profile data is appended; a different directory starts new files and old data is not used.

## Architecture notes from the capacity page (modernized VMware)
- Create a new Recovery Services vault for the replication appliance; do not reuse an existing vault.
- The appliance hosts the proxy, discovery, re-protection and process servers, among others; the process server caches and compresses data before sending to Azure.
- Maximum recovery point retention is 15 days; app-consistent snapshots can be taken every 1 to 12 hours; the RPO threshold only drives monitoring alerts.

## Verify
- [ ] Report reviewed, incompatible VMs remediated or excluded, wave plan sized to bandwidth documented.

## Checked
Method: docs-checked 2026-11-09 against the site-recovery-deployment-planner page (read through the version-history section) and the site-recovery-plan-capacity-vmware page (architecture, URLs and replication-process sections). Dropped the exact command lines and operation names (profiling, report and throughput syntax is on later sections not read), the Hyper-V overview and Azure-to-Azure support-matrix sources (404 or not read), and the per-disk churn and quota claims.
