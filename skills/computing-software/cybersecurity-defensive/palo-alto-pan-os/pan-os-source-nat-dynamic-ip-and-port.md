---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-source-nat-dynamic-ip-and-port
name: pan-os-source-nat-dynamic-ip-and-port
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [source-nat, pan-os, snat, dynamic-ip-and-port, dipp, nat-policy, interface-address]
level: practitioner
status: draft
description: "Configure PAN-OS source NAT with DIPP, static IP and interface translation, and size the port pool correctly."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/networking/nat/source-nat-and-destination-nat"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: outbound internet access for private subnets with predictable translation.

```
configure
set rulebase nat rules snat-outbound from trust to untrust source 10.0.0.0/8 destination any service any
set rulebase nat rules snat-outbound source-translation dynamic-ip-and-port interface-address interface ethernet1/1
commit
```
Pooled variant:
```
set rulebase nat rules snat-pool from trust to untrust source 10.0.0.0/8 source-translation dynamic-ip-and-port translated-address 203.0.113.20-203.0.113.23
```
Static IP (1:1, optional bidirectional): `source-translation static-ip translated-address 203.0.113.30 bi-directional yes`.

Facts
- DIPP gives roughly 64k ports per translated address, multiplied by an oversubscription factor that depends on the model (confirm). Heavy NAT'd clients can exhaust ports: add addresses or lower oversubscription.
- NAT rules do not permit traffic; a security rule must also allow it, matched on pre-NAT addresses and the post-NAT destination zone.

Gotchas
- Ordering: first match wins, so static rules go above the generic DIPP rule.
- When using a routed block of addresses, make sure upstream routes it to the firewall or enable proxy ARP on the interface.

## Verify
```
test nat-policy-match from trust to untrust source 10.1.1.5 destination 198.51.100.7 protocol 6 destination-port 443
show session all filter nat source
show running nat-policy
show running global-ippool
```
Sessions should list the translated source and port.
