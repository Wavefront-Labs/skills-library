---
id: computing-software.systems-network-administration.virtualisation.esxi-management-network-rollback-and-recovery
name: esxi-management-network-rollback-and-recovery
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vds-rollback, management-network-recovery, dcui, vds, esxi-networking, vmware, esxi]
level: advanced
status: docs-checked
description: "Use vSphere network rollback and the DCUI restore options to recover an ESXi host cut off by a bad vDS or management network change."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2032908
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Management network rollback and recovery

**Goal:** get a host back on the network after a change that dropped its management connection.

## Automatic rollback
Since vSphere 7.0, vCenter rolls back an invalid host or distributed switch networking change, including a change that disconnects a host. Rollback is enabled by default and can be enabled or disabled at the vCenter Server level. It works on both standard and distributed switches.

## DCUI recovery
At the host console (DCUI), the Network Restore Options menu offers **Restore vDS** to repair the distributed switch configuration from the host side. For a vDS management network failure, a host can also be given a standard switch with a proper management network configuration so vCenter can manage it again; the "Network Adapters" and "VLAN" DCUI options are greyed out until management networking is moved to a standard switch.

Where hardware allows, the KB suggests a standard switch for management and a vDS for other traffic (at least four adapters: two per switch).

## After recovery
Reconnect the host in vCenter and reconcile the distributed switch configuration. For ESXi Shell recovery commands, consult the ESXCLI command reference for your release.

## Verify
vmk0 reachable, host connected in vCenter, no network configuration warnings on the vDS.

## Checked

2026-10-28

Confirmed: Broadcom KB 311145 (network rollback and recovery in vSphere 7.0 and later): enabled by default, vCenter-level switch, standard and distributed switches, Restore vDS from the DCUI, greyed-out DCUI options, VSS-plus-VDS design.

Removed or corrected: 30 s timeout and advanced setting names, trigger list, shell recovery commands (esxcli reference not readable), Restore Standard Switch and Restore Network Settings detail.

Method: documentation only; no commands were run.
