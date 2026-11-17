---
id: computing-software.networking-hardware-and-wireless.open-vswitch.userspace-tso-and-tx-steering
name: userspace-tso-and-tx-steering
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, tso, userspace-tso, tx-steering, checksum-offload, dpdk, segmentation, vhost-user]
level: advanced
status: docs-checked
description: "Enable TCP segmentation offload in the Open vSwitch userspace datapath with userspace-tso-enable, set guest TSO and checksum flags, and choose tx-steering thread or hash."
sources:
  - https://docs.openvswitch.org/en/latest/topics/userspace-tso/
  - https://docs.openvswitch.org/en/latest/topics/userspace-tx-steering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Userspace TSO and tx-steering
TSO:
`ovs-vsctl set Open_vSwitch . other_config:userspace-tso-enable=true` then restart ovs-vswitchd.

Guests must use offloads: in the guest `ethtool -K eth0 sg on` then `ethtool -K eth0 tso on` (scatter-gather is a prerequisite), and give QEMU the virtio-net device options `csum=on,guest_csum=on,guest_tso4=on,guest_tso6=on`. The NIC needs a DPDK PMD that supports TSO.

When a TSO packet goes out a port that cannot segment, the userspace datapath segments it in software; `ovs-appctl coverage/read-counter dp_packet_gso` counts these. Supported tunnels for TSO are VxLAN, Geneve and GRE.

tx-steering:
Per Interface, `other_config:tx-steering` chooses how packets spread over tx queues. `thread` (default, also when unset) maps PMD threads to tx queues and a thread never uses more than one queue of a port; `hash` spreads packets over all the port's tx queues by 5-tuple hash, always takes the tx lock and may cost performance (useful for vhost-user ports with more guest queues than PMD threads).
`ovs-vsctl set Interface <iface> other_config:tx-steering=hash`; set it back to `thread` to disable hash mode.

Verify: `ovs-vsctl get Open_vSwitch . other_config:userspace-tso-enable` returns "true", and for a vhost port `ovs-vsctl get interface vhost0 status:tx_tcp_seg_offload` returns "true".

Gotcha: changing userspace-tso-enable needs a daemon restart (default false); a guest already connected before the restart has no TSO until its QEMU process is stopped and started again.

## Checked

2026-11-09. Confirmed against the Userspace Datapath TSO and Userspace Tx packet steering pages: userspace-tso-enable and restart, QEMU csum/tso device options, ethtool steps, software segmentation fallback, thread and hash modes and commands, status:tx_tcp_seg_offload. Removed: host_tso4, software checksum fallback, and the throughput claim (not on the pages).
Method: documentation only; no commands were run.
