---
id: computing-software.systems-network-administration.network-design.virtual-switching-and-nfv
name: virtual-switching-and-nfv
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, vswitch, nfv, vds, open-vswitch, sr-iov, virtual-networking]
level: practitioner
status: gated
description: "Design hypervisor networking: standard vs distributed vSwitches, uplink teaming, VLAN trunking to hosts, Open vSwitch, SR-IOV, and NFV virtual routers/firewalls."
sources:
  - https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-networking/GUID-35B40B0B-0C13-43B2-BC85-18C9C91BE2D4.html
  - https://docs.openvswitch.org/en/latest/
  - https://www.etsi.org/technologies/nfv
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v-virtual-switch/hyper-v-virtual-switch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual switching and NFV

## Virtual switches
| Platform | Switch | Notes |
|---|---|---|
| VMware | vSS (per host), vDS (vCenter-managed) | vDS is managed centrally from vCenter |
| Hyper-V | Hyper-V vSwitch with SET (switch embedded teaming) | SET is Microsoft's documented vSwitch teaming option |
| KVM/Proxmox | Linux bridge, Open vSwitch | Open vSwitch (OVS) |
| Cloud | provider-managed | security groups replace vSwitch ACLs |

## Uplink design
- Two or more physical NICs per traffic type, to two ToR switches.
- Teaming: the vSwitch teaming policy must match the physical switch config (static EtherChannel, LACP or none); a mismatch causes MAC flaps or black holes.
- Trunk the needed VLANs to hosts (`switchport trunk allowed vlan`), portfast trunk/edge on the
  switch ports, BPDU guard on.
- Separate management, vMotion/live migration, storage and VM traffic by VLAN and NIOC/QoS.
- Jumbo frames end to end for storage/vMotion if used (vSwitch, vmkernel, physical switch).

## SR-IOV and DPDK
SR-IOV gives VMs a virtual function of the NIC: near line-rate, low latency, but bypasses the
vSwitch (no vSwitch policy, limited vMotion). Use for NFV data planes and latency-sensitive apps (gated: unconfirmed, source is paywalled or blocked).

## NFV
Virtual routers/firewalls/load balancers
replacing appliances. ETSI NFV covers lifecycle management of virtualised network functions on NFV infrastructure platforms. Plan vCPU pinning, NUMA locality,
hugepages and licensed throughput; HA needs anti-affinity rules across hosts.

## Verify
- [ ] Pull each host uplink: VMs keep connectivity; vSwitch teaming policy matches physical switch config; vMotion between hosts keeps VLAN and policy.

## Checked

- Date: 2026-10-28
- Confirmed: Hyper-V virtual switch page lists Switch Embedded Teaming (SET); ETSI NFV page: lifecycle management of virtualised network functions hosted on NFV infrastructure platforms.
- Removed: vDS feature list, LBFO replacement claim, OVS protocol list, VMware teaming policy names, NFV product names.
- Gated: the SR-IOV behaviour paragraph (the VMware and Open vSwitch pages fetched were index pages without that detail).
Method: documentation only; no commands were run.
