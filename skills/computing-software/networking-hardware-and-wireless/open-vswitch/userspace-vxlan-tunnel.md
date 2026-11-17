---
id: computing-software.networking-hardware-and-wireless.open-vswitch.userspace-vxlan-tunnel
name: userspace-vxlan-tunnel
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, vxlan, tnl-route, userspace, netdev, tunnel, arp-cache, egress-port-range]
level: advanced
status: docs-checked
description: "Run a VXLAN tunnel on the userspace (netdev) datapath: tunnel endpoint IP on the physical bridge, ovs/route and tnl/arp commands, UDP source port range, and verification."
sources:
  - https://docs.openvswitch.org/en/latest/howto/userspace-tunneling/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# userspace vxlan tunnel
Bridges use the userspace datapath:
```
ovs-vsctl --may-exist add-br br-phy -- set Bridge br-phy datapath_type=netdev
ovs-vsctl add-br br-int -- set Bridge br-int datapath_type=netdev
```
Attach the physical NIC to `br-phy` (`ovs-vsctl --timeout 10 add-port br-phy eth1`), then give the physical bridge the tunnel endpoint address (kernel-managed NIC case; the how-to also flushes the NIC's own address and brings it up):
```
ip addr add 172.168.1.1/24 dev br-phy
ip link set br-phy up
```
Tunnel port on the integration bridge:
`ovs-vsctl add-port br-int vxlan0 -- set interface vxlan0 type=vxlan options:remote_ip=172.168.1.2`

Routing and neighbours (userspace datapath keeps its own tables):
- `ovs-appctl ovs/route/show`; add a missing route: `ovs-appctl ovs/route/add 172.168.1.1/24 br-phy` (the output bridge must be an OVS bridge)
- `ovs-appctl ovs/route/lookup IP`, `ovs/route/del ip/plen`
- `ovs-appctl tnl/arp/show` (alias `tnl/neigh/show`), `tnl/arp/flush`, `tnl/arp/set br-phy IP MAC`
- `ovs-appctl tnl/arp/aging [seconds]` (1 to 3600)
- `ovs-appctl tnl/egress_port_range 40000 50000` sets the UDP source port range; with no arguments it prints it.
- `ovs-appctl tnl/ports/show` lists tunnel ports being listened on.

Verify: ping the remote VM address across the tunnel; `ovs-appctl dpif/show` for datapath ports and `ovs-appctl dpif/dump-flows <datapath>` for datapath flows.

Gotcha: `br-phy` exists so the datapath can use the kernel stack for routing and ARP; if the tunnel route is missing from `ovs/route/show`, add it explicitly. A DPDK NIC is not visible to `ip`, so use `add-port ... type=dpdk` instead of the kernel commands or connectivity is lost.

## Checked

2026-11-09. Confirmed against the Connecting VMs Using Tunnels (Userspace) how-to and the tunneling commands in ovs-vswitchd(8): bridge creation with datapath_type=netdev, vxlan port, br-phy purpose, route, ARP, ports and egress_port_range commands, aging range 1 to 3600, dpif/show and dpif/dump-flows. Removed: the claim that encapsulation fails without the route (not stated). Reworded: the dump-flows argument.
Method: documentation only; no commands were run.
