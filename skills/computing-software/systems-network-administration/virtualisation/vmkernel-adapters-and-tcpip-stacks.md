---
id: computing-software.systems-network-administration.virtualisation.vmkernel-adapters-and-tcpip-stacks
name: vmkernel-adapters-and-tcpip-stacks
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmkernel-adapter, tcpip-stack, vmkernel, vmotion-stack, provisioning-stack, vmk, vmkping, vsphere-networking, vmware, esxi, vsphere]
level: practitioner
status: draft
description: "Lay out ESXi VMkernel adapters per service (management, vMotion, vSAN, storage, FT, replication), use the vMotion/provisioning TCP/IP stacks and test them with vmkping."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0/setting-up-vmkernel-networking.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VMkernel adapters and TCP/IP stacks

**Goal:** each host service has its own VMkernel interface, subnet and VLAN, routed
correctly, so one traffic type cannot accidentally ride another's path.

## Services that need a vmk
| Service | Typical layout |
|---|---|
| Management | vmk0, routed management VLAN |
| vMotion | dedicated non-routed VLAN; use the **vMotion TCP/IP stack** if it must cross L3 |
| Provisioning (cold migration, cloning, snapshots of powered-off VMs) | optional, **provisioning stack** |
| vSAN | dedicated VLAN, jumbo frames end to end |
| iSCSI / NFS | one vmk per path for iSCSI port binding; NFS on the storage VLAN |
| Fault Tolerance logging, vSphere Replication, NVMe-oF | own vmk if used |

## TCP/IP stacks
The default stack has one default gateway for all vmks on it. If vMotion needs to route
between sites, put its vmk on the **vMotion stack**, which has its own gateway, DNS and
routing table. Once any vmk on a host uses the vMotion stack, vMotion is disabled on the
default stack for that host. Stacks are chosen at vmk creation and cannot be changed
later; recreate the vmk.

```sh
esxcli network ip interface add -i vmk1 -p vMotion-PG -N vmotion
esxcli network ip interface ipv4 set -i vmk1 -t static -I <IP> -N <MASK>
esxcli network ip netstack list
esxcli network ip route ipv4 add -N vmotion -n default -g <GW>
esxcli network ip interface tag add -i vmk1 -t VMotion      # enable the service
esxcli network ip interface list
```
Static routes on the default stack (`esxcli network ip route ipv4 add -n <net>/<len> -g <gw>`)
are the alternative for routed storage, but are easy to forget on new hosts; put them
in the host profile.

## Testing
```sh
vmkping -I vmk1 -S vmotion <peer-vmotion-ip>
vmkping -I vmk2 -d -s 8972 <peer-vsan-ip>     # jumbo test: don't fragment, 9000 minus headers
```
A `-d -s 8972` failure with plain ping working means an MTU mismatch somewhere in the path.

## Verify
`esxcli network ip interface tag get -i vmkN` shows exactly the intended services per vmk;
vmkping succeeds between every host pair on each service network.
