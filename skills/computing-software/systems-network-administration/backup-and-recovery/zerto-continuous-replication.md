---
id: computing-software.systems-network-administration.backup-and-recovery.zerto-continuous-replication
name: zerto-continuous-replication
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [zerto, continuous-data-protection, journal, vpg, failover-test, dr-orchestration]
level: advanced
status: draft
description: "Operate Zerto for DR: ZVM and VRA deployment, virtual protection groups, journal sizing, failover test, live failover, move and failback, with common pitfalls."
sources:
  - https://help.zerto.com/
  - https://help.zerto.com/bundle/Admin.VC.HTML/page/Zerto_Virtual_Replication_Overview.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zerto continuous replication

Zerto (HPE) gives journal-based continuous replication with RPOs in seconds and built-in orchestration.

## Components
- **ZVM** (Zerto Virtual Manager, appliance) per site, paired with the vCenter/Hyper-V/cloud.
- **VRA** (Virtual Replication Appliance) on every host: taps writes at the hypervisor and sends them to the remote VRA.
- **Journal** at the target: every write kept for the journal history (e.g. 1 hour to 30 days), giving any-point-in-time recovery.

## Virtual Protection Groups (VPGs)
Group VMs that must recover together and consistently (app + DB). Per VPG: target site/cluster, datastore, journal history and size limit, recovery networks for **live** and **test**, boot order with delays, re-IP rules, scripts.

## Journal sizing
Journal ≈ write rate × history; set a hard limit and a warning (%) so a burst does not fill the datastore. Zerto shrinks history when the limit is hit.

## Operations
- **Failover Test**: boots VMs from any checkpoint into the test network; replication continues. Stop test when done; records a report for auditors.
- **Live Failover**: real DR, choose checkpoint (latest or before corruption), commit policy (auto-commit after N minutes or manual), reverse protection.
- **Move**: planned migration with source shutdown, no data loss.
- **Failback**: reverse protection then Move back.
- Tag checkpoints before risky changes ("pre-upgrade") to make them easy to find.

## Gotchas
- VRA needs IPs and resources per host; host maintenance requires VRA awareness.
- Ransomware writes are replicated instantly; recover from a checkpoint before infection.
- Monitor RPO and journal history alerts; bandwidth issues show as rising RPO.

## Verify
Quarterly failover test per critical VPG with the Zerto test report saved; RPO dashboard green.
