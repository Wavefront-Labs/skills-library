---
id: computing-software.networking-hardware-and-wireless.open-vswitch.afxdp-ports
name: afxdp-ports
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, afxdp, af-xdp, xdp, userspace, netdev, xdp-mode, libbpf]
level: advanced
status: docs-checked
description: "Add AF_XDP ports to an Open vSwitch userspace bridge: --enable-afxdp, type=afxdp, n_rxq, pmd-rxq-affinity, xdp-mode and requirements."
sources:
  - https://docs.openvswitch.org/en/latest/intro/install/afxdp/
  - https://docs.openvswitch.org/en/latest/topics/dpdk/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AF_XDP ports
Experimental. Requirements: Linux kernel 5.4 or newer (or a distribution kernel with the features backported) with CONFIG_BPF, CONFIG_BPF_SYSCALL and CONFIG_XDP_SOCKETS, libbpf, and libxdp if libbpf is newer than 0.6; build OVS with `./boot.sh && ./configure --enable-afxdp`.

Bridge and port (userspace datapath):
```
ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev
ovs-vsctl add-port br0 enp2s0 -- set interface enp2s0 type="afxdp" options:n_rxq=4
```
The how-to sets the PMD cores first and then pins queues to them, with the NIC queue count matched to `n_rxq` (`ethtool -L enp2s0 combined 4`):
```
ethtool -L enp2s0 combined 4
ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=0x36
ovs-vsctl add-port br0 enp2s0 -- set interface enp2s0 type="afxdp" options:n_rxq=4 other_config:pmd-rxq-affinity="0:1,1:2,2:3,3:4"
```
`pmd-rxq-affinity` is optional (otherwise the system assigns queues) and `n_rxq` defaults to 1.

`options:xdp-mode` is `best-effort` (default, best of the supported modes), `native-with-zerocopy`, `native` or `generic`; check what best-effort chose:
`ovs-vsctl get interface ens802f0 status:xdp-mode`

Verify: `ovs-vsctl show` lists the port with `type: afxdp` and its options; for debugging enable `ovs-appctl vlog/set netdev_afxdp::dbg`.

Gotcha: AF_XDP has no QoS support because it bypasses the Linux TC layer; the page suggests the OpenFlow meter action as a work-around.

## Checked

2026-11-09. Confirmed against the Open vSwitch with AF_XDP install page: experimental status, kernel and library requirements, configure flag, bridge and port commands, n_rxq and pmd-rxq-affinity examples and defaults, xdp-mode values and status:xdp-mode, vlog debug command, no-QoS limitation. Removed: the pmd-rxq-show verify step and the unserved-queues claim (not on the pages). Reworded: the libbpf or libxdp requirement.
Method: documentation only; no commands were run.
