---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-one-reports-and-alarms
name: veeam-one-reports-and-alarms
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-one-reports, veeam-one, alarms, backup-monitoring, protected-vms-report]
level: practitioner
status: draft
description: "Use Veeam ONE to monitor backups: key alarms, the protected and unprotected VM reports, RPO compliance, scheduling report delivery and tuning alarm noise."
sources:
  - https://helpcenter.veeam.com/docs/one/monitor/about.html
  - https://helpcenter.veeam.com/docs/one/reporter/about.html
  - https://helpcenter.veeam.com/docs/one/monitor/alarms.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Veeam ONE reports and alarms

Veeam ONE = Monitor (real-time alarms) + Reporter (scheduled reports) + Client/Web. Add the B&R servers and the vCenter/Hyper-V hosts so it can compare "what exists" with "what is protected".

## Alarms worth keeping on
- Backup job state, Job disabled, Backup copy RPO, Immutability state changes.
- Repository free space (warning 20%, error 10%).
- **Possible ransomware activity** (CPU/disk/network pattern on VMs) and malware detection events (v12+).
- Backup server configuration backup state, Veeam services state.
- Suppress noise: disable VM-level performance alarms you do not act on; assign alarms to email groups by severity.

## Reports to schedule
| Report | Audience | Frequency |
|---|---|---|
| Protected VMs | Backup team, auditors | Weekly |
| VMs with no recent backup / Unprotected VMs | Backup team | Daily |
| Backup Job Historical Information | Team lead | Weekly |
| Restore Operator Activity | Security/audit | Monthly |
| Capacity Planning for Backup Repositories | Infra manager | Monthly |
Reporter > Reports > select > Schedule, delivery to email or file share (PDF/Excel).

## RPO checks
Set the RPO in the "Protected VMs" report parameters (e.g. 24 hours); VMs with an older last restore point are listed as unprotected.

## Gotchas
- Veeam ONE must be upgraded before B&R.
- Data collection runs on a schedule; recently added VMs can show as unprotected until the next collection.

## Verify
Daily unprotected report arrives and is empty or has tickets; a test alarm (stop a job) emails the right group.
