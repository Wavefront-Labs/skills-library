---
id: computing-software.systems-network-administration.cisco-networking.static-nat-and-port-forwarding
name: static-nat-and-port-forwarding
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, nat, static-nat, port-forwarding, ip-nat-inside, ip-nat-outside, extendable]
level: practitioner
status: draft
description: "Publish an inside server with static one-to-one NAT or a static PAT port forward on IOS, including the extendable keyword and testing from outside."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13772-12.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-addr-consv.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static NAT and port forwarding

## Mark interfaces first
```
interface GigabitEthernet0/0/0
 ip nat outside
interface GigabitEthernet0/0/1
 ip nat inside
```
Without both, nothing translates and `show ip nat translations` stays empty.

## One-to-one (spare public IP)
```
ip nat inside source static 10.1.1.10 203.0.113.10
```
All ports map; the router answers ARP for 203.0.113.10 on the outside interface (if the
address is on that subnet). If the public block is routed to you instead, no ARP is needed.

## Port forward on the interface address
```
ip nat inside source static tcp 10.1.1.10 443 interface GigabitEthernet0/0/0 443
ip nat inside source static tcp 10.1.1.11 443 203.0.113.10 8443 extendable
```
- `extendable` is required when the same inside IP appears in more than one static
  mapping (IOS adds it automatically in many cases).
- Forwarding to the interface address works with DHCP-assigned WAN IPs.
- An inbound ACL on the outside interface is checked before NAT translates, so it must
  permit the **public** address and port, not the inside one.

## Gotchas
- Testing from inside the LAN to the public IP fails without hairpin NAT (separate skill).
- Static entries do not age out; `clear ip nat translation *` does not remove them.
- Overlapping with PAT overload on the same interface address: static port mappings take
  precedence for those ports.

## Verify
```
show ip nat translations | include 10.1.1.10
show ip nat statistics
```
From an outside host: `curl -v https://203.0.113.10:8443/`; hit counters on the outside ACL.
- [ ] Translation shows `tcp 203.0.113.10:8443 10.1.1.11:443`, external test succeeds.
