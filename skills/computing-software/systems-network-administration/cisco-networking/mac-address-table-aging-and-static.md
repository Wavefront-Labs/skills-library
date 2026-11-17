---
id: computing-software.systems-network-administration.cisco-networking.mac-address-table-aging-and-static
name: mac-address-table-aging-and-static
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, mac-address-table, mac-learning, frame-switching, mac-aging, aging-time, static-mac, cam-table, arp-timeout, unicast-flooding, mac-address-table-static, drop]
level: practitioner
status: docs-checked
description: "Tune MAC learning on Catalyst switches: aging time vs ARP timeout, static and drop MAC entries, per-VLAN settings and the asymmetric-routing flood that a mismatch causes."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/administering_the_device.html
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6000-series-switches/23563-143.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAC address table: aging and static entries

A switch learns the source MAC of every frame on the ingress port and VLAN, and forwards to the
port in the table. When no entry matches the destination MAC in the VLAN, the unicast frame is
sent out all forwarding ports in that VLAN: **unknown unicast flooding**. Each VLAN keeps its own
logical address table, so a MAC known in one VLAN is unknown in another until learned there.

## Inspect
```
show mac address-table dynamic vlan 20
show mac address-table address 0011.2233.4455
show mac address-table interface Gi1/0/7
show mac address-table count vlan 20
show mac address-table aging-time
show mac address-table static
```

## Aging
- Default dynamic aging is 300 seconds (Catalyst 9300, IOS XE 17.9). Syntax:
  `mac address-table aging-time [0 | 10-1000000] [routed-mac | vlan vlan-id]`. The aging interval is
  global by default; `vlan` sets it per VLAN. `0` disables aging. STP can accelerate aging per VLAN.
- Static addresses are never aged out.
- Cisco's flooding document names asymmetric routing as a common cause: the return path
  bypasses the switch, so it never sees the host's source MAC in that VLAN, the entry ages out and
  traffic is flooded until the host sends something (an ARP broadcast, for example).
  Symptoms: bulk traffic reaches ports that are not party to the conversation and saturates
  slow links.
- Cisco's usual approach is to bring the router ARP timeout and the switch MAC aging time close
  to each other so ARP refreshes the entry before it ages out. Find the router's ARP timeout on
  the SVI and set the switch aging time per VLAN near it, for example
  `mac address-table aging-time 14400 vlan 20` if that timeout were 4 hours.

## Static and drop entries
```
mac address-table static 0011.2233.4455 vlan 20 interface Gi1/0/7   ! pin a host
mac address-table static 0011.2233.4466 vlan 20 drop                 ! drop a MAC
```
A static unicast entry takes one interface at a time (repeat the command with the same MAC and
VLAN to add more). The `drop` form drops packets with that source or destination MAC. Static
entries are not lost when the device resets (they are in the configuration; save it).

## Learning limits and moves
- `mac address-table notification mac-move` plus `show mac address-table notification mac-move`
  report MAC moves between ports (see mac-address-table-notifications).
- If the forwarding table overflows, new addresses cannot be learned and traffic to them is
  flooded; a host sending frames with many different source MACs can cause this, and port
  security limits MACs learned on untrusted ports.
- `no mac address-table learning vlan <id>` disables learning on a VLAN (2 to 4094). Cisco
  recommends it only for VLANs with two ports, because otherwise every packet is flooded, and
  warns against it on a VLAN with an SVI. MAC learning stays on at secure ports.

## Gotchas
- `clear mac address-table dynamic` (all), or with `address`, `interface` or `vlan`, removes
  entries, and traffic is flooded until they are relearned; prefer the narrow forms.
- Repeated STP topology changes shorten aging and cause near-constant flooding; see the STP
  topology change skill.

## Verify
- [ ] `show mac address-table aging-time` matches the design per VLAN.
- [ ] No sustained unknown-unicast flooding (a capture on an access port should not repeatedly
      show unicast frames for other hosts).
- [ ] Static entries appear in `show mac address-table static`.

## Checked
2026-11-08. Confirmed against the Catalyst 9300 17.9 System Management guide ("Administering the
Device": MAC address table, default aging, aging-time syntax and range, static and drop entries,
learning disable guidelines, clear and show commands) and Cisco's "Unicast Flooding in Switched
Campus Networks" (asymmetric routing, TCN, table overflow, ARP/aging alignment). Removed
unsupported claims: the 4-hour ARP default and `arp timeout 270`, NLB unicast mode, `show sdm
prefer`, port-security interaction, vPC and stack behaviour. The "4 hours" in the example is an
illustration of matching, not a stated default. The Layer 2 guide index source was dropped.
Method: documentation only; no commands were run.
