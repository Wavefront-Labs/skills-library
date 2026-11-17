---
id: computing-software.systems-network-administration.linux.open-vswitch-bridges-ovs-vsctl
name: open-vswitch-bridges-ovs-vsctl
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, openvswitch, ovs-vsctl, ovs-ofctl, ovs-bridge, vlan-trunk, sdn]
level: practitioner
status: docs-checked
description: "Build and debug Open vSwitch bridges: ovs-vsctl bridges, ports, VLAN access and trunk ports, bonds, internal ports, persistence via NetworkManager/ifupdown, and flow inspection."
sources:
  - https://docs.openvswitch.org/en/latest/faq/configuration/
  - https://github.com/openvswitch/ovs/blob/main/utilities/ovs-vsctl.8.in
  - https://docs.openvswitch.org/en/latest/howto/libvirt/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Open vSwitch bridges with ovs-vsctl

**Goal:** a software switch with VLANs, bonds and OpenFlow, typically for KVM/libvirt, OpenStack or Proxmox hosts.

## Install and inspect
```bash
ovs-vsctl show                      # bridges, ports, interfaces, errors
ovs-vsctl list-br; ovs-vsctl list-ports br0
```

## Build a bridge
```bash
ovs-vsctl add-br br0
ovs-vsctl add-port br0 ens19                     # uplink (trunk by default: all VLANs)
ovs-vsctl add-port br0 vnet0 tag=20              # access port in VLAN 20
ovs-vsctl set port ens19 trunks=20,30            # restrict trunk (Port table column `trunks`)
ovs-vsctl add-port br0 mgmt20 tag=20 -- set Interface mgmt20 type=internal   # internal port for a host IP on VLAN 20
ip addr add 192.0.2.10/24 dev mgmt20 && ip link set mgmt20 up
ovs-vsctl add-bond br0 bond0 ens19 ens20 lacp=active bond_mode=balance-tcp   # at least two interfaces; bond_mode defaults to active-backup
```
Moving the host's only uplink into a bridge drops its IP: do it from the console or in one command chain that also moves the address to an internal port.

## Persistence
OVS keeps bridge and port configuration in its own database (ovs-vswitchd.conf.db(5)), which `ovs-vsctl` edits; host IP addresses on internal ports are set with ordinary network tools and need persistent config. Use one of:
- NetworkManager: `ovs-bridge`, `ovs-port` and `ovs-interface` connections (settings include `ovs-port.tag`, `ovs-port.lacp` active/off/passive, `ovs-port.bond-mode` active-backup/balance-slb/balance-tcp).
- netplan: an `openvswitch:` mapping on the device (netplan reports an error if Open vSwitch is not installed).
- Your distribution's ifupdown or networkd integration, if any (check its documentation).

## libvirt guest interface on OVS
```xml
<interface type='bridge'>
  <source bridge='br0'/>
  <virtualport type='openvswitch'/>
</interface>
```
The interface type must be `bridge`; `<virtualport type='openvswitch'/>` marks the bridge as an Open vSwitch bridge.

## Debug flows
```bash
ovs-ofctl dump-flows br0                # OpenFlow flow table
ovs-appctl fdb/show br0                 # MAC/VLAN pairs learned, with port and age
ovs-appctl ofproto/trace br0 in_port=1,dl_vlan=20,dl_dst=52:54:00:aa:bb:cc   # ofproto/trace BRIDGE FLOW: where would this packet go
ovs-appctl bond/show bond0; ovs-appctl lacp/show
```
If `ovs-vsctl show` lists an error on a port, check that the interface it names exists.

## Verify
- [ ] VM on tag=20 reaches the VLAN 20 gateway; `ofproto/trace` shows the expected output port.
- [ ] Bridge configuration and the host IP survive a reboot.

## Checked

Date: 2026-10-25. Documentation release: Open vSwitch main (last commit 2026-10-23): utilities/ovs-vsctl.8.in, vswitchd/ovs-vswitchd.8.in, vswitchd/vswitch.xml, ofproto/ofproto-unixctl.man, Documentation/faq/configuration.rst, Documentation/howto/libvirt.rst, Documentation/topics/bonding.rst; netplan and NetworkManager settings text; read 2026-10-25.
Confirmed: `add-br`, `add-port` with `tag=` (access port, trunk by default), `add-bond` (at least two interfaces), `type=internal` port example, `list-ports`; Port `trunks`, `lacp` and `bond_mode` columns (balance-tcp valid, bond mode defaults to active-backup); `ovs-appctl bond/show`, `lacp/show`, `fdb/show`, `ofproto/trace BRIDGE FLOW`; libvirt `<virtualport type='openvswitch'/>` with interface type bridge; NetworkManager OVS settings; netplan `openvswitch`.
Removed as unconfirmed: package and service names, the conf.db path, log path, the exact "could not open network device" error, ifupdown stanzas, `ovs-dpctl show`, `dpctl/dump-flows`, the libvirt `<portgroup>` network XML, and the ovs-vsctl.8.txt link (replaced with the source file).

Method: documentation only; no commands were run.
