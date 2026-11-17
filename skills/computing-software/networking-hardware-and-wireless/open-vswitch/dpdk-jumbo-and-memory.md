---
id: computing-software.networking-hardware-and-wireless.open-vswitch.dpdk-jumbo-and-memory
name: dpdk-jumbo-and-memory
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, dpdk, jumbo-frames, mtu-request, per-port-memory, shared-mempool-config, mempool, mbuf, hugepages]
level: advanced
status: docs-checked
description: "Configure jumbo frames and mbuf memory for Open vSwitch DPDK ports: mtu_request, guest MTU, per-port-memory, shared-mempool-config and how the default shared mempool is sized."
sources:
  - https://docs.openvswitch.org/en/latest/topics/dpdk/jumbo-frames/
  - https://docs.openvswitch.org/en/latest/topics/dpdk/memory/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DPDK jumbo frames and memory
Jumbo frames: DPDK ports default to MTU 1500; change the Interface mtu_request attribute (OVS 2.6 and later).
`ovs-vsctl set Interface dpdk-p0 mtu_request=9000`
For vhost-user guests, enable mergeable buffers (`mrg_rxbuf=on` on the virtio-net-pci device). Where the guest uses the Linux kernel virtio driver, raise the guest interface MTU too: `ip link set eth1 mtu 9000`. MTU counts the IP packet only, so 9000 corresponds to a 9018 byte frame.

Memory models:
- Default shared model: ports with the same MTU and socket ID share a mempool. Mempools hold 262144 mbufs when MTU is 1500 or greater (16384 below 1500). If memory is short the request is halved down to 16384.
- `other_config:per-port-memory=true` gives each device its own mempool; set it before `dpdk-init=true`, otherwise restart the daemon.
- `other_config:shared-mempool-config=9000,1500:1,6000:1` sets the MTUs that shared mempools are based on, per NUMA node, so ports with different MTUs can reuse a mempool. Entries without a node apply to all nodes.

Sizing: memory per mempool is mbuf count times mbuf size, and the mbuf size is always larger than the MTU. Example from the docs: MTU 9000 uses a 10176 byte mbuf, so a 262144 mbuf shared pool needs about 2667 MB. Allocate the hugepage memory before enabling per-port mode.

## Checked
2026-11-04. Confirmed against the Jumbo Frames and DPDK Device Memory Models pages: default MTU, mtu_request, mergeable buffers, the guest MTU command, shared and per-port models, the mbuf counts, the per-port-memory ordering rule, shared-mempool-config format and the sizing example. Removed because the pages did not confirm them: the dpdk-socket-mem advice, the verify line using get Interface mtu and error, and the hugepage failure gotcha.
Method: documentation only; no commands were run.
