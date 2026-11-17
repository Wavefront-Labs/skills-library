---
id: computing-software.systems-network-administration.cisco-networking.port-acls-on-switchports
name: port-acls-on-switchports
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9300, port-acl, pacl, vacl, racl, acl-precedence, voice-vlan]
level: practitioner
status: docs-checked
description: "Apply IP and MAC ACLs to Catalyst 9300 Layer 2 ports (PACLs): the one-IP-plus-one-MAC rule, precedence against VLAN maps and router ACLs, trunk and voice VLAN scope."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ipv4_acls.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ipv6_acls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Port ACLs (PACLs) on switchports

Scope: Catalyst 9300 IOS XE 17.9 (IPv4 ACLs and IPv6 ACLs chapters). Other platforms differ.

## What a port ACL is
An ACL applied to a Layer 2 interface. Supported types: standard IP (source addresses), extended IP (source,
destination and optional protocol) and MAC extended (source and destination MAC plus optional protocol type).
Port ACLs are supported on physical interfaces and EtherChannel interfaces but not on EtherChannel member
interfaces. The guide does not require routing to be enabled.

## Config
```
ip access-list extended KIOSK-PORT
 permit ...
 deny ip any any
interface gigabitethernet1/0/30
 switchport mode access
 ip access-group KIOSK-PORT in
```
Syntax from the guide: `ip access-group {access-list-number | name} {in | out}` on a Layer 2 interface makes it a
port ACL (on a Layer 3 interface it is a router ACL). `show access-lists [number | name]` shows the ACL content,
`show ip interface interface-id` the ACL applied, `show mac access-group [interface interface-id]` the MAC ACLs.
Applying an undefined ACL means the device acts as if no ACL were applied and permits all packets.

## One IP list and one MAC list
At most one IP access list and one MAC access list per Layer 2 interface; the IP list filters only IP packets and
the MAC list only non-IP packets. Applying a new list of the same kind replaces the old one. See mac-acls-on-catalyst.

## Order of ACL types
When VLAN maps, port ACLs and router ACLs exist on the same switch, precedence from greatest to least is: ingress
traffic port ACL, VLAN map, router ACL; egress traffic router ACL, VLAN map, port ACL. Example from the guide:
with an input port ACL and a VLAN map, packets received on ports with a port ACL are filtered by the port ACL; other
packets by the VLAN map. A VLAN map is not defined by direction.

## Scope gotchas
- On a trunk the port ACL filters traffic on all VLANs present on the trunk.
- On a port with a voice VLAN the ACL filters both data and voice VLANs, so the rules must also cover phone traffic.
- Direction: the guide says port ACLs can be applied inbound and outbound, in each direction per list type, but the
  figure caption also says "inbound only"; confirm on the device you run.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 IPv4 ACLs chapter at Supported ACLs, ACL
Precedence, Port ACLs, MAC ACLs on a Layer 2 Interface, Applying an IPv4 ACL to an Interface and Applying a MAC ACL to a
Layer 2 Interface (found by searching for "port ACL" and reading those sections; the whole chapter was not read), and the
matching ACL Precedence text in the IPv6 ACLs chapter. Removed as unconfirmed: `access-group mode prefer port`/merge,
the ISE dACL placeholder statement, TCAM exhaustion, the kiosk rules (bootps, domain, 10.0.0.80), the
`ipv6 traffic-filter` PACL line (the IPv6 chapter shows it on routed interfaces), ARP handling and the `| include`
and per-entry statistics checks. The inbound/outbound inconsistency in the guide is stated rather than resolved.
