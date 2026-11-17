---
id: computing-software.systems-network-administration.cisco-networking.span-vlan-sources-and-filters
name: span-vlan-sources-and-filters
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, span, span-vlan-source, span-filter, span-direction, encapsulation-replicate, monitor-session, port-mirroring]
level: practitioner
status: draft
description: "Mirror the right traffic with SPAN: VLAN vs port sources, rx/tx/both direction and duplicates, VLAN and ACL filters on trunk sources, and destination port behaviour."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_span_and_rspan.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPAN VLAN sources, direction and filters

## Port vs VLAN source
```
monitor session 1 source interface Gi1/0/10 both
monitor session 1 source vlan 20 rx
monitor session 1 destination interface Gi1/0/48
```
- Port source: everything on that port (in the chosen direction).
- VLAN source (VSPAN): all ports in that VLAN on this switch. Only `rx` is supported on some
  platforms for VLAN sources; traffic routed between VLANs may appear twice.

## Direction and duplicates
- `rx`: frames received on the source; `tx`: frames sent; `both`: each.
- Mirroring two ports that talk to each other with `both` produces each packet twice (once as tx of
  one, once as rx of the other). Same with a VLAN source plus a routed path. Mirror only one side,
  or use `rx` on all sources (captures each frame once as it enters the switch).
- Duplicates confuse TCP analysis (dup ACK/retransmission noise); `editcap -d` removes exact
  duplicates afterwards.

## Filtering a trunk source
```
monitor session 1 source interface Te1/1/1 both
monitor session 1 filter vlan 20,30
```
Only VLANs 20 and 30 from the trunk are mirrored. ACL-based filtering (FSPAN) on Catalyst 9k:
```
ip access-list extended SPAN-FILTER
 permit ip host 10.20.0.5 any
 permit ip any host 10.20.0.5
monitor session 1 filter ip access-group SPAN-FILTER
```
Filtering at the source reduces oversubscription of the destination port.

## Destination port behaviour
- Stops being a normal switchport: no STP, no learning, no traffic in by default.
- `encapsulation replicate` keeps the original 802.1Q tags on mirrored trunk traffic (otherwise
  tags may be stripped and you cannot tell VLANs apart).
- `ingress vlan 99` lets the capture host send traffic (e.g. management) back in; otherwise it is
  isolated.

## Verify
```
show monitor session 1 detail
show interfaces Gi1/0/48 | include output rate|drops
```
- [ ] Capture on the destination shows the expected hosts once per packet, with VLAN tags if
  needed, and output drops on the destination stay at zero.
