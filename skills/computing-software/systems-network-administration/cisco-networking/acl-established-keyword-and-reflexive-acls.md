---
id: computing-software.systems-network-administration.cisco-networking.acl-established-keyword-and-reflexive-acls
name: acl-established-keyword-and-reflexive-acls
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, acl, established-keyword, reflexive-acl, evaluate, stateful-filtering, return-traffic]
level: practitioner
status: draft
description: "Filter return traffic on IOS routers with the established keyword or reflexive ACLs (reflect/evaluate), their limits, and when to use ZBFW instead."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_data_acl/configuration/xe-16/sec-data-acl-xe-16-book/sec-create-filter-tcp.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_data_acl/configuration/xe-16/sec-data-acl-xe-16-book/sec-reflexive-acl.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The established keyword and reflexive ACLs

## established
```
ip access-list extended OUTSIDE-IN
 permit tcp any 10.0.0.0 0.255.255.255 established
 deny ip any any log
```
`established` matches TCP segments with ACK or RST set. It is **stateless**: an attacker can craft
ACK packets that pass (ACK scans). It does nothing for UDP or ICMP. Use only as a crude filter.

## Reflexive ACLs (session-based, still IOS)
```
ip access-list extended INSIDE-OUT
 permit tcp 10.0.0.0 0.255.255.255 any reflect MIRROR timeout 300
 permit udp 10.0.0.0 0.255.255.255 any reflect MIRROR timeout 60
 permit icmp 10.0.0.0 0.255.255.255 any reflect MIRROR
ip access-list extended OUTSIDE-IN
 evaluate MIRROR
 deny ip any any log
interface GigabitEthernet0/0       ! outside
 ip access-group INSIDE-OUT out
 ip access-group OUTSIDE-IN in
```
Outbound sessions create temporary mirrored entries; inbound traffic is permitted only if it
matches one. Entries expire after the timeout or on TCP FIN/RST.

## Limits
- Must be named extended ACLs; `reflect` on a permit, `evaluate` in another ACL.
- No support for protocols that open secondary channels (FTP active, SIP media): ports differ.
- Does not inspect sequence numbers or payload; per-packet process cost on old platforms.
- IOS XE: reflexive ACLs are supported on some platforms only; Zone-Based Firewall (ZBFW) is the
  stateful replacement with inspection of L7 protocols.

## Verify
```
show ip access-lists MIRROR       ! temporary entries with remaining time
show ip access-lists OUTSIDE-IN
```
- [ ] Inbound connection attempts to inside hosts are denied; outbound sessions return.
