---
id: computing-software.networking-hardware-and-wireless.open-vswitch.bfd-cfm-lldp-monitoring
name: bfd-cfm-lldp-monitoring
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, bfd, cfm, lldp, auto-attach, link-monitoring, cfm-mpid]
level: advanced
status: docs-checked
description: "Enable link-fault detection on Open vSwitch interfaces with BFD or CFM, enable LLDP/auto-attach, and use ovs-appctl bfd/show, cfm/show and fault overrides."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bfd cfm lldp monitoring
BFD (set per Interface; not enabled by default):
- `ovs-vsctl set interface gre0 bfd:enable=true`
- `bfd:min_rx` default 1000 ms; `bfd:min_tx` default 100 ms; `bfd:mult` 1 to 255, default 3; `bfd:decay_min_rx` 0 disables the feature.
- `bfd:forwarding_if_rx`, `bfd:cpath_down` (default false), `bfd:check_tnl_key` (true accepts only control messages with tunnel key zero; by default any key is accepted) and `bfd:oam` (marks BFD packets as OAM in tunnels that carry such a bit, such as Geneve) are true/false options.

CFM: `ovs-vsctl set Interface eth0 cfm_mpid=1` enables it (standard range 1 to 8191).
- `other_config:cfm_interval` default 1000 ms (standard mode allows 3, 10, 100, 1000, 10000, 60000, 600000 and rounds other values down; extended mode allows up to 65,535 ms).
- `other_config:cfm_extended` default false; `cfm_demand`; `cfm_ccm_vlan` 1 to 4095; `cfm_ccm_pcp` 1 to 7.

LLDP / Auto Attach: `lldp:enable` on an Interface (disabled by default); the AutoAttach table has `system_name`, `system_description` and `mappings` (ISID 0 to 16777215 to VLAN 0 to 4095).

Runtime:
- `ovs-appctl bfd/show [iface]`, `cfm/show [iface]`
- `ovs-appctl bfd/set-forwarding [iface] true|false|normal` and `cfm/set-fault [iface] true|false|normal` override fault status for testing.

Use `normal` afterward to revert an override to standard behaviour.

## Checked
2026-11-09. Partial read (the BFD, CFM, LLDP and AutoAttach sections) of ovs-vswitchd.conf.db(5): bfd keys and defaults (min_rx 1000, min_tx 100, mult 3 in 1 to 255, decay_min_rx 0 disables), cfm_mpid 1 to 8191, cfm_interval, cfm_extended, cfm_demand, cfm_ccm_vlan 1 to 4095, cfm_ccm_pcp 1 to 7, lldp:enable off by default, AutoAttach system_name, system_description and mappings (ISID 0 to 16,777,215, VLAN 0 to 4,095). Read bfd/show, bfd/set-forwarding, cfm/show, cfm/set-fault in ovs-vswitchd(8). Removed: the unsourced true/false defaults for three BFD options and the verify step.
Method: documentation only; no commands were run.
