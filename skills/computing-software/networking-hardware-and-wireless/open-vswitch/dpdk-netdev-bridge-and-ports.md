---
id: computing-software.networking-hardware-and-wireless.open-vswitch.dpdk-netdev-bridge-and-ports
name: dpdk-netdev-bridge-and-ports
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, dpdk, netdev, dpdk-init, dpdk-devargs, vfio-pci, hugepages, dpdk-socket-mem, rx-steering]
level: advanced
status: draft
description: "Set up DPDK in Open vSwitch: dpdk-init and memory options, bind a NIC to vfio-pci, create a netdev bridge and dpdk port with dpdk-devargs, flow control and rx-steering."
sources:
  - https://docs.openvswitch.org/en/latest/intro/install/dpdk/
  - https://docs.openvswitch.org/en/latest/howto/dpdk/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DPDK bridge and ports
Enable and tune (other_config on the Open_vSwitch table; restart ovs-vswitchd after changing init):
```
ovs-vsctl set Open_vSwitch . other_config:dpdk-init=true
ovs-vsctl set Open_vSwitch . other_config:dpdk-socket-mem="1024,0"
ovs-vsctl set Open_vSwitch . other_config:dpdk-lcore-mask=0x2
```
`dpdk-init` takes false, true or try; `dpdk-extra` passes raw EAL args.

Bind the NIC to a userspace driver:
`driverctl set-override 0000:07:00.0 vfio-pci` or `dpdk-devbind --bind=vfio-pci 0000:07:00.0`.

Create the bridge and port:
```
ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev
ovs-vsctl add-port br0 dpdk-p0 -- set Interface dpdk-p0 type=dpdk options:dpdk-devargs=0000:01:00.0
```
Representor ports use devargs with a representor suffix. Per-port: `options:tx-flow-ctrl`, `rx-flow-ctrl`, `flow-ctrl-autoneg`; `options:rx-steering=rss+lacp` steers LACP to a separate queue.

Remove a port: `ovs-appctl netdev-dpdk/detach 0000:01:00.0` after deleting it.

Verify: `ovs-vsctl list interface dpdk-p0` shows `link_state=up`, and `ovs-vsctl get Interface dpdk-p0 error` is empty.

Gotcha: `rx-steering` cannot be combined with hw-offload.
