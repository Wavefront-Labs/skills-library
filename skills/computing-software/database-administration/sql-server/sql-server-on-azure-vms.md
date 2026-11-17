---
id: computing-software.database-administration.sql-server.sql-server-on-azure-vms
name: sql-server-on-azure-vms
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, sql-iaas-agent, sql-server-azure-vm, premium-ssd-v2, storage-pools, automated-patching, azure-vm-sizing]
level: advanced
status: docs-checked
description: "Run SQL Server on Azure VMs well: VM and disk choice, storage layout with caching rules, the SQL IaaS Agent extension features, and HA options."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/virtual-machines/windows/performance-guidelines-best-practices-checklist
  - https://learn.microsoft.com/en-us/azure/azure-sql/virtual-machines/windows/sql-server-iaas-agent-extension-automate-management
  - https://learn.microsoft.com/en-us/azure/azure-sql/virtual-machines/windows/performance-guidelines-best-practices-storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server on Azure VMs

Choose VMs when you need OS-level access or control that PaaS options do not give.

## VM size
Memory-optimised with high memory-to-vCore ratio and good IO limits: E-series (Ebdsv5 for higher
remote storage throughput), M-series for very large memory.
The **VM-level** IOPS/throughput cap
often limits before disks do: check both.

## Storage layout
| Files | Disk | Host caching |
|---|---|---|
| Data | Premium SSD (P30/P40 or smaller keeps cache support) striped across disks, or Premium SSD v2 (Ebdsv5/Ebsv5) | see the storage best-practices page |
Format data disks with a 64-KB allocation unit (not the temporary D: drive, which defaults to 4 KB).

## SQL IaaS Agent extension
Register an existing VM with the extension:
```bash
az sql vm create -n <vm> -g <rg> --license-type PAYG --sql-mgmt-type Full
```
Benefits listed in the extension article: portal management, automated backup, automatic patching, Azure Key Vault integration, tempdb configuration, Defender for Cloud integration, flexible licensing (Azure Hybrid Benefit and pay-as-you-go), SQL best practices assessment, I/O analysis.

## HA and DR
- Choose the availability group, failover cluster instance and backup design from the HA/DR articles for SQL Server on Azure VMs; their limits are not restated here.

## Gotchas
- Place data files on data disks, not the temporary D: drive.

## Checked

2026-10-28. Confirmed in the Azure SQL VM best-practice checklist, storage and IaaS Agent extension pages: 64-KB allocation unit and 4 KB default on the temporary D: drive, P30/P40 or smaller disks for cache support, Ebdsv5/Ebsv5 with Premium SSD v2, the extension benefits table, and az sql vm create --license-type / --sql-mgmt-type (checked against the az reference). Removed: E16-4ds_v5 constrained-size example, per-file caching table rows, Ultra caching claim, Lightweight-mode claim, DR free licence claim, HA bullet details, burst-credit and IFI/LPIM gotchas, the claim that PaaS lacks specific features.

Method: documentation only; no commands were run.

## Verify
SQL best practices assessment reviewed in the portal; throughput tested against the VM and disk limits.
