---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-meters
name: ofctl-meters
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, add-meter, meter-bands, meter, rate-limit, ovs-ofctl, openflow13]
level: advanced
status: docs-checked
description: "Create OpenFlow meters with ovs-ofctl add-meter and dump-meters, drop bands with rate and burst_size, and apply them in flows with meter:N (OpenFlow 1.3 instruction, 1.5 action)."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
  - https://docs.openvswitch.org/en/latest/howto/tc-offload/
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl meters
Meter commands work only with switches supporting OpenFlow 1.3 or later; enable it in ovs-ofctl with `-O` and in the switch with the Bridge `protocols` column.

Commands (ovs-ofctl(8)): `add-meter switch meter`, `mod-meter switch meter`, `del-meters switch [meter]` (all if omitted or `all`), `dump-meters switch [meter]`, `meter-stats switch [meter]` (`meter=id` or `meter=all`), `meter-features switch`.

Meter spec (repeated fields: last instance honoured):
- `meter=id` required (except for meter-stats); an integer for user meters, plus the virtual meters `all`, `controller` (packets sent to the controller) and `slowpath` (packets sent to OVS userspace).
- `kbps` or `pktps` sets the unit for `rate` and `burst_size`; a unit is required for add-meter and mod-meter.
- `burst` enables burst support through `burst_size`; `stats` enables collection of meter and band statistics.
- `bands=` needs at least one band for add-meter and mod-meter and must come after all other fields. Each band starts with `type=drop` (drop packets over the rate), then `rate=value`, optional `burst_size=size` (only if `burst` is set; otherwise the switch picks a value). If several bands' rates are exceeded, the band with the highest rate among them applies.

Example from the tc-offload how-to:
```
ovs-ofctl -O OpenFlow13 add-meter br0 "meter=1 pktps bands=type=drop rate=1"
ovs-ofctl -O OpenFlow13 add-flow br0 "priority=10,in_port=ovs-p0,udp actions=meter:1,normal"
```
`meter:meter_id` is an instruction in OpenFlow 1.3 and an action in 1.5; OVS restricts the meter action to be first in an action list and excludes it from action sets. Meter datapath support: userspace datapath from OVS 2.7, kernel datapath from 2.10; the 1.5 action form from 2.12.

TC offload (how-to): meters offload to TC automatically when possible and need the tc-police action in the kernel. Each meter maps to one TC police action; indexes 0x10000000 to 0x1fffffff are reserved for this, and `tc action ls action police` lists them. Limitations: TC counts only the number of dropped packets, so meter statistics show 0 for byte_count; packets handled by an upcall before the meter flow is installed are not policed.

## Checked
2026-11-04. Confirmed against ovs-ofctl(8) (Meter Table Commands, Meter Syntax), ovs-actions(7) (meter action) and the TC offload how-to. Corrected `del-meter` to `del-meters`; removed the Verify line.
Method: documentation only; no commands were run.
