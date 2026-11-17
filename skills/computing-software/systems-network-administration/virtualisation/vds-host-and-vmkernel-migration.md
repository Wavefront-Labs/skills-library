---
id: computing-software.systems-network-administration.virtualisation.vds-host-and-vmkernel-migration
name: vds-host-and-vmkernel-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-networking, distributed-switch, vds, vds-migration, vmkernel-migration, rollback, ephemeral-binding, vmware, esxi, vsphere]
level: advanced
status: draft
description: "Move hosts, uplinks, vmk0 and VMs from a standard switch to a vSphere Distributed Switch without losing management, using network rollback and an ephemeral port group."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=2032908
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating hosts and VMkernel adapters to a vDS

**Goal:** get management, vMotion, storage and VM traffic onto a distributed switch with
zero lost hosts, one uplink at a time.

## Prepare
1. Create the vDS (version matching the oldest host), uplink count, and port groups with
   the **same VLANs** as the vSS port groups.
2. Create an **ephemeral-binding** management port group on the vDS (or keep a vSS
   recovery path). Static-binding port groups need vCenter to assign ports; if vCenter
   runs on this vDS and goes down you cannot reconnect it.
3. Confirm **network rollback** is on (`config.vpxd.network.rollback` = true, default):
   vCenter reverts a change that cuts a host off within ~30 s.
4. Check the physical switch ports carry every VLAN for both uplinks.

## Migrate (Add and Manage Hosts wizard)
1. Add the hosts; assign **one** physical NIC per host to the vDS uplink, leaving the
   other on the vSS so management stays up.
2. Migrate VMkernel adapters: vmk0 → vDS management port group; vmk1 vMotion, vmk2
   iSCSI/NFS → their port groups. iSCSI port-bound vmks must keep exactly one active
   uplink in the new teaming policy.
3. Migrate VM networking (wizard or per-VM). vCenter VM itself: move it separately and
   carefully to the ephemeral port group.
4. Test, then move the second physical NIC to the vDS and remove the empty vSS.

## Recovery when it goes wrong
- Host disconnected: DCUI → Network Restore Options → **Restore Standard Switch**,
  which creates vSwitch0 with vmk0 on a chosen NIC.
- vDS out of sync on a host (yellow warning): Rectify vSphere Distributed Switch on
  host, or remove and re-add the host.
- Export the vDS config (Settings → Export Configuration) before and after; it can
  recreate the switch in a rebuilt vCenter.

## Gotchas
- MTU mismatch between vDS and physical switch passes pings but breaks vMotion/storage;
  enable vDS health check (VLAN and MTU, teaming) temporarily to find it.
- LACP on the vDS needs a different procedure (see the LACP skill): do not migrate a
  host into a LAG while its only uplink is in it.

## Verify
Every host shows all uplinks on the vDS, vmk adapters on vDS port groups, the vSS removed,
vDS health check green, and a test vMotion between two migrated hosts succeeds.
