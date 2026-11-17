---
id: computing-software.systems-network-administration.cisco-networking.vlan-access-maps-vacl
name: vlan-access-maps-vacl
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, vacl, vlan-access-map, vlan-filter, acl, intra-vlan-filtering, security]
level: practitioner
status: draft
description: "Filter traffic inside a VLAN with VLAN access maps: match/action sequences, vlan filter binding, the implicit drop, and how VACLs interact with RACLs and PACLs."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ipv4_acls.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLAN access maps (VACLs)

Router ACLs on an SVI only see routed traffic. A VACL applies to every packet bridged or routed
into or out of a VLAN, including host-to-host traffic in the same subnet.

## Build one
```
ip access-list extended BLOCK-TELNET
 permit tcp any any eq 23
ip access-list extended ALL-IP
 permit ip any any

vlan access-map VLAN20-POLICY 10
 match ip address BLOCK-TELNET
 action drop log
vlan access-map VLAN20-POLICY 20
 match ip address ALL-IP
 action forward
vlan access-map VLAN20-POLICY 30
 action forward                     ! catch-all for non-IP (ARP!) if no match clause

vlan filter VLAN20-POLICY vlan-list 20
```
Logic: the ACL selects packets (`permit` = match), the map entry decides `forward` or `drop`.
A `deny` in the ACL means "not matched by this entry", not "drop".

## Implicit drop
A packet that matches no entry is dropped. A map with only drop entries blackholes the VLAN,
including ARP. Always end with a forward-everything entry with no match clause, or match a MAC ACL
for ARP:
```
mac access-list extended ARP
 permit any any 0x0806 0x0
```

## Verify
```
show vlan access-map VLAN20-POLICY
show vlan filter
show access-lists BLOCK-TELNET
show platform software fed switch active acl counter hardware   ! Cat9k drop counters
```

## Interaction with other ACLs
Order on ingress for a routed packet: PACL (port) then VACL (input VLAN) then RACL (SVI in), then
RACL out, VACL output VLAN. A packet must pass all of them. VACLs apply in both directions; there is
no `in`/`out`.

## Gotchas
- Capture use: `action forward capture` with `switchport capture` on older platforms; on Cat9k use
  SPAN with ACL filters instead.
- VACLs consume TCAM like other ACLs; check `show platform hardware fed switch active fwd-asic
  resource tcam utilization`.
- IPv6 traffic needs `match ipv6 address` entries or it hits the catch-all.
- Test in a maintenance window: a missing forward entry drops the whole VLAN instantly.

## Verify
- [ ] Hosts in the VLAN still resolve ARP and reach the gateway.
- [ ] Blocked flow fails and counters on the drop entry increase.
