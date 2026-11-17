---
id: computing-software.systems-network-administration.virtualisation.vds-private-vlans
name: vds-private-vlans
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [private-vlan, pvlan, isolated-pvlan, community-pvlan, vds, vmware, vsphere]
level: advanced
status: docs-checked
description: "Private VLAN concepts on a vSphere distributed switch: primary, promiscuous, isolated and community groups, tagging, and why the physical switches must be PVLAN aware."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1010691
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Private VLANs on a vDS

**Goal:** understand how isolated, community and promiscuous private VLANs behave, so VM
isolation holds across hosts.

## Model (from the Broadcom article)
- A private VLAN extends the VLAN standard to split a logical broadcast domain into private
  groups. Hosts in a PVLAN cannot be seen by others, except through the promiscuous PVLAN.
- **Primary PVLAN:** the original VLAN being divided. Secondary PVLANs exist only inside it.
- **Secondary PVLANs:** each has its own VLAN ID, and packets are tagged with that ID like a
  normal VLAN. The physical switch derives the behaviour (isolated, community or
  promiscuous) from the VLAN ID in each packet.
- **Promiscuous:** a node can send to and receive from any node in the other secondary
  VLANs of the same primary. Routers are typically attached to promiscuous ports.
- **Isolated:** a node can only send to and receive from the promiscuous PVLAN.
- **Community:** a node can talk to others in the same community secondary PVLAN and to the
  promiscuous PVLAN.

## Notes that matter in practice
- Promiscuous PVLANs have the same VLAN ID for primary and secondary.
- Community and isolated traffic travels tagged as its secondary PVLAN. Nothing is
  encapsulated: one tag per packet, using the standard 802.1Q tag.
- Traffic between VMs in the same PVLAN on different ESX hosts goes through the physical
  switch, so that switch must be PVLAN aware and configured to let the secondary PVLANs
  reach their destination.
- Switches learn MAC addresses per VLAN, so a VM appears to be in more than one VLAN to the
  physical switch; this is why every physical switch connected to ESX hosts using PVLANs must
  be PVLAN aware. "Aware" means the switch has PVLAN mapping and is not itself configured for
  PVLAN on the interface facing the ESXi host; confirm the exact switch configuration with
  the switch vendor.

## Checked
Date: 2026-11-07. Read the whole Broadcom KB article "Private VLAN (PVLAN) on vNetwork
Distributed Switch not working - Concept Overview". All statements above come from it.
Removed as not on the page: the vDS and port-group configuration steps, the example VLAN IDs,
the switch configuration listing, "PVLAN is vDS only", the DHCP/ARP gotcha, the same-host
isolation claim and the ping Verify test. The linked "About vSphere Networking" and
"Private VLANs" pages were not opened.
Method: documentation only; no commands were run.
