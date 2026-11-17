---
id: computing-software.networking-hardware-and-wireless.opnsense.high-availability-sync
name: high-availability-sync
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [high-availability, carp, config-sync, pfsync, failover]
level: advanced
status: docs-checked
description: "OPNsense HA workflow and settings: on-demand config sync, cron replication, preempt, dialup disconnect, state sync interface and status page."
sources: ["https://docs.opnsense.org/manual/hacarp.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# High availability and configuration sync

OPNsense high availability uses CARP for hardware failover: if the primary loses an interface or goes offline, the secondary takes over and existing connections continue with minimal interruption. CARP-type Virtual IPs are required for automatic failover.

Workflow: configuration is not pushed automatically. Apply and test changes on the master first, then synchronise the backup on command from the HA status page. This keeps the backup in a known good state, so in an emergency you can still switch to it. If you prefer periodic replication, add a cron job on the primary under System > Settings > Cron with the command "HA update and reconfigure backup", scheduled for example once daily outside office hours. It runs only when all CARP interfaces are MASTER, so a broken primary cannot overwrite the active master.

Settings (System > High Availability > Settings):
- Disable preempt: unchecked by default, which is advised. Preempt makes multiple CARP interfaces act as a group, all backup or all master.
- Disconnect dialup interfaces: a CARP backup disconnects PPP-type interfaces and reconnects them on becoming master.
- Synchronize all states via: replicates the state table so connections survive failover. Choose a dedicated interface to avoid state manipulation or loss under congestion. From 24.7 a Sync compatibility selector exists; keep both nodes on the same version.
- Configuration synchronization: configure it only on the master. A backup should never contain the settings, or an admin could accidentally sync the backup over the master. Using a different theme on the master helps tell the nodes apart.

The status page connects to the configured backup, lists its services, and lets you update it and restart services; the refresh button does both at once.

## Checked

2026-11-03. Confirmed against the OPNsense High Availability manual page: CARP failover, workflow, cron replication and its MASTER condition, preempt, dialup disconnect, state sync and the 24.7 Sync compatibility selector, configuration synchronization advice, status page. Nothing removed.

Method: documentation only; no commands were run.
