---
id: computing-software.networking-hardware-and-wireless.open-vswitch.hw-offload-tc
name: hw-offload-tc
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, hw-offload, tc, tc-flower, tc-policy, smartnic, offload, representor]
level: advanced
status: docs-checked
description: "Enable Open vSwitch hardware offload through Linux TC with other_config:hw-offload, choose tc-policy, verify offloaded flows, and offload meters via police actions."
sources:
  - https://docs.openvswitch.org/en/latest/howto/tc-offload/
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TC hardware offload
Enable (default is false; changing it requires restarting the daemon; experimental):
`ovs-vsctl set Open_vSwitch . other_config:hw-offload=true`

Policy: `other_config:tc-policy` (default `none`, only relevant with hw-offload) is `none` (software rule plus hardware offload rule), `skip_sw` (offload rule to hardware only) or `skip_hw` (software rule only).

Check what is offloaded: `ovs-appctl dpctl/dump-flows type=offloaded` (ovs-dpctl cannot dump hardware offloaded flows).

Meters are offloaded automatically when possible and need the tc-police action in the kernel; each meter maps to one TC police action (indexes 0x10000000-0x1fffffff are reserved). Create a meter with `ovs-ofctl -O OpenFlow13 add-meter` (see ofctl-meters), reference it with `meter:1`, and list TC actions with `tc action ls action police`.

Limitations noted in the howto:
- TC does not support conntrack ALGs: flows with the ALG keyword in `ct()` are not offloaded, so disable TC offload if ALG support is needed.
- Offloaded flow byte counts omit the L2 header.
- Byte counts of dropped packets under an offloaded meter show 0.
- Packets handled by an upcall before the offload rule exists are not policed.

Verify: `ovs-appctl dpctl/dump-flows type=offloaded` lists the flows offloaded to hardware after traffic starts.

Gotcha: `rx-steering` on DPDK ports is mutually exclusive with `hw-offload`; if both are enabled rx-steering falls back to the default rss mode.

## Checked

2026-11-09. Confirmed against the Flow Hardware offload with Linux TC flower how-to, the Open_vSwitch and Interface tables of ovs-vswitchd.conf.db(5) and the dpctl/dump-flows type list in ovs-vswitchd(8): hw-offload default and restart, tc-policy values and default, meter commands and police action index range, limitations, rx-steering exclusion. Removed: the offloaded:yes output claim (not on the pages). Added: the ovs-vswitchd(8) source.
Method: documentation only; no commands were run.
