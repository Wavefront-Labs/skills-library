---
id: computing-software.systems-network-administration.backup-and-recovery.unprotected-workload-detection
name: unprotected-workload-detection
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [unprotected-vms, protection-coverage, backup-monitoring, auto-protection, backup-reporting, coverage-gap]
level: practitioner
status: draft
description: "Detect workloads with no backup: reconcile hypervisor and cloud inventories against backup tool coverage, tag-driven auto-protection, documented exclusions and new-VM alerts."
sources:
  - https://helpcenter.veeam.com/docs/one/reporter/protected_vms.html
  - https://learn.microsoft.com/en-us/azure/backup/backup-azure-auto-enable-backup
  - https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unprotected workload detection

**Goal:** no production workload exists without a backup unless someone decided so in writing.

## Reconcile inventory with protection
1. **Inventory**: vCenter (`Get-VM`), Hyper-V/Proxmox lists, cloud (Azure Resource Graph, AWS Config), physical servers from the CMDB, SaaS tenants, databases.
2. **Protected list** from backup tools:
   - Veeam: Veeam ONE "Protected VMs" report (lists unprotected VMs), or PowerShell over jobs and backups (`Get-VBRJob`, `Get-VBRJobObject`, `Get-VBRBackup`).
   - Azure: `az backup item list` per vault, Backup center.
   - AWS: `aws backup list-protected-resources`.
3. Join by unique ID (VM UUID/MoRef, Azure resource ID, ARN), not by name.
4. Output: unprotected = inventory minus protected minus approved exclusions.

## Prevent gaps
- **Tag- or container-based selection** so new workloads are protected automatically: Veeam jobs on vSphere tags, folders or clusters; AWS Backup tag selections; Azure Policy auto-enable backup for tagged VMs.
- Require a `backup` tag (or `backup=none` with ticket reference) at provisioning; enforce with policy (Azure Policy deny/audit, AWS SCP/Config rules).
- Freshness check: protected but last successful restore point older than RPO counts as unprotected.

## Exclusions
Keep a register: workload, reason (stateless, rebuilt from code, test), approver, review date. Unregistered exclusions are gaps.

## Alerting
Daily report; alert when a production-tagged workload exists for more than 24 hours without a successful backup.

## Gotchas
- Excluding disks inside a protected VM (e.g. data disks) leaves partial protection; report disk-level coverage for databases.
- Shared or replicated workloads may be protected via another site; record which copy is the protected one.

## Verify
The unprotected list is empty or matches the exclusion register, and a newly created test VM is flagged or auto-protected within a day.
