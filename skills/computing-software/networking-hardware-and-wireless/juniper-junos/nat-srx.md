---
id: computing-software.networking-hardware-and-wireless.juniper-junos.nat-srx
name: nat-srx
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, srx-nat, source-nat, destination-nat, static-nat]
level: practitioner
status: draft
description: "Configure SRX source NAT (interface and pool), destination NAT and static NAT with proxy-arp."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAT on SRX
Goal: translate addresses on an SRX.

```
set security nat source rule-set SNAT from zone trust
set security nat source rule-set SNAT to zone untrust
set security nat source rule-set SNAT rule R1 match source-address 10.0.0.0/8
set security nat source rule-set SNAT rule R1 then source-nat interface
set security nat destination pool WEB address 10.0.0.20/32 port 443
set security nat destination rule-set DNAT from zone untrust
set security nat destination rule-set DNAT rule R1 match destination-address 203.0.113.20/32
set security nat destination rule-set DNAT rule R1 then destination-nat pool WEB
set security nat proxy-arp interface ge-0/0/0.0 address 203.0.113.20/32
```

- Order of processing: static NAT, destination NAT, route lookup, security policy, source NAT. The policy is written with the post-DNAT destination address.
- A permit policy is still required for the translated flow.

Gotcha: DNAT works but nothing answers ARP because there is no proxy-arp for the public address (not on the interface subnet). Static/destination NAT addresses in the interface subnet usually need `proxy-arp`.

## Verify
- `show security nat source rule all` and `show security nat destination summary` show hits; `show security flow session` displays translated addresses.
