---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-replica-failover-and-failback
name: veeam-replica-failover-and-failback
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [replica-failover, failover-plan, failback, veeam-replication, re-ip, network-mapping, veeam]
level: advanced
status: docs-checked
description: "Operate Veeam replicas: failover to a restore point, undo or permanent failover, planned failover, failover plans with ordering and re-IP, and failback with commit."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/failover.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/failback.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/failover_plan.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replica failover and failback (Veeam)

**Goal:** switch to VM replicas at the DR site and later return to production.

## Failover
- Veeam rolls the replica back to the chosen restore point (reverts to the matching snapshot in the replica chain), powers it on, and the state changes from Ready to Failover.
- It can be used for disaster recovery or to test recoverability, and can run while the source VM is running (the source stays powered on in a test). If source and replica share a network, consider disconnecting the source temporarily to avoid IP or machine-name conflicts; SureReplica is the alternative test method.
- Veeam stops all replication activity for the source VM until its replica returns to Ready.
- Changes made in the Failover state are written to the delta file of the snapshot you rolled back to.
- Always use Veeam to fail over; powering on a replica manually may disrupt later replication or lose data.
- Failover is an intermediate step: finalise with **undo failover**, **permanent failover** or **failback**.

## Failover plans
- A plan fails over dependent VMs one by one as a group: you set the order and the interval to wait before starting the next VM (for example so a DNS server is running first). It must be created in advance.
- When started you choose the latest state or a point in time; the closest restore points are used. Source VMs are not powered off.
- VMs whose replicas are already in Failover or Failback state are skipped.
- At most 10 VMs start simultaneously; extra VMs wait for earlier ones to finish failing over.
- Undo failover can be done for the whole group; permanent failover and failback must be done per VM.

## Failback
Switches back from the replica to production and sends the changes made on the replica to the production VM. Options: the source VM in its original location; a VM already recovered to a new location (recover it first, for example from backup); or a VM recovered from the replica to a new location or with different settings.
- The first two transfer only differences; the third transfers the whole VM, so use it only if the source cannot be used or restored from backup.
- Two phases: (1) synchronise the production VM with the replica while the replica keeps running (can take long for large VMs); (2) switch processes to the production VM, turn off the replica and send changes made since phase 1. Phase 2 can start automatically, at a scheduled time or manually.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Failover", "Failback" and "Failover Plans" (build 13.x).
Removed (not on those pages): the re-IP and network mapping details, permanent-failover semantics ("restore points removed"), planned failover description, snapshot-growth warning, quarterly test advice, Verify section. The "commit failback" step was not on the pages read.
Method: documentation only; no commands were run.
