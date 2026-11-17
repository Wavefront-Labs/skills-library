---
id: computing-software.systems-network-administration.cisco-networking.mac-acls-on-catalyst
name: mac-acls-on-catalyst
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9300, mac-acl, ethertype, non-ip-traffic, port-acl, layer-2-security]
level: practitioner
status: docs-checked
description: "Filter non-IP traffic on Catalyst 9300 Layer 2 ports with named MAC extended ACLs: entry syntax, one-MAC-list rule, physical-port-only limit and how to display them."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ipv4_acls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAC ACLs

Scope: Catalyst 9300 IOS XE 17.9 (IPv4 ACLs chapter, MAC ACL sections).

## Config
```
mac access-list extended mac1
 deny any any decnet-iv
 permit any any
interface gigabitethernet1/0/2
 mac access-group mac1 in
```
Entry syntax from the guide:
`{deny | permit} {any | host source-MAC | source-MAC mask} {any | host dest-MAC | dest-MAC mask} [type mask | lsap lsap mask | aarp | amber | dec-spanning | decnet-iv | diagnostic | dsm | etype-6000 | etype-8042 | lat | lavc-sca | mop-console | mop-dump | msdos | mumps | netbios | vines-echo | vines-ip | xns-idp | 0-65535] [cos cos]`
- `type mask`: an arbitrary EtherType of an Ethernet II or SNAP packet (decimal, hex or octal) with an optional
  don't-care mask; `lsap lsap mask`: an LSAP of an IEEE 802.2 packet; `cos` is 0 to 7.
- Interface command: `mac access-group {name} {in | out}`; the guide says port ACLs are supported inbound and
  outbound.

## Which traffic a MAC ACL sees
A MAC ACL on a Layer 2 interface filters non-IP traffic; the IP access list filters only IP packets. So a port MAC
ACL does not filter IPv4 or IPv6 packets by MAC.

## Rules
- At most one IP access list and one MAC access list per Layer 2 interface. A new MAC ACL replaces the old one.
- `mac access-group` is valid only on a physical Layer 2 interface, not on EtherChannel port channels.
- In a VLAN map, non-IP protocols are access-controlled by MAC address and EtherType using MAC VLAN maps; IP
  traffic is not controlled by MAC VLAN maps.
- An undefined ACL applied to an interface is treated as not applied (all packets permitted).
- Precedence among port ACL, VLAN map and router ACL: see port-acls-on-switchports.

## Check
`show mac access-group [interface interface-id]` displays the MAC access list applied to the interface or to all
Layer 2 interfaces; `show access-lists [number | name]` displays ACL contents.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 IPv4 ACLs chapter: MAC ACLs on a Layer 2
Interface, ACL Supported Types, Port ACLs, VLAN Maps (non-IP paragraph), Creating a Named MAC Extended ACL, Applying a
MAC ACL to a Layer 2 Interface and the monitoring table (sections located by search, then read; not the whole chapter).
Removed as unconfirmed: ethertype examples (0x8137 IPX, 0x0806, 0x86dd, 0x88cc), the OUI mask example, "inbound only
on many platforms", ARP special handling, TCAM utilisation, `match mac address` and scapy test. The security command
reference cited earlier was not read and was dropped from sources.
