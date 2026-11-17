---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-destination-nat-and-uturn
name: pan-os-destination-nat-and-uturn
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [destination-nat, pan-os, dnat, u-turn-nat, port-forwarding, hairpin, static-nat]
level: practitioner
status: draft
description: "Publish internal servers through PAN-OS destination NAT and handle hairpin U-turn access, with the pre-NAT and post-NAT policy rule."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/networking/nat/destination-nat"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: expose a server at a public address and let internal users reach it by the same name.

External access:
```
configure
set address web-public ip-netmask 203.0.113.10/32
set address web-internal ip-netmask 10.1.1.10/32
set rulebase nat rules dnat-web from untrust to untrust source any destination web-public service service-https
set rulebase nat rules dnat-web destination-translation translated-address web-internal translated-port 443
set rulebase security rules allow-web-in from untrust to dmz source any destination web-public application ssl action allow
commit
```
The NAT rule's `to` zone is the zone of the PRE-NAT destination (untrust). The security rule uses the POST-NAT zone (dmz) with the PRE-NAT destination address (203.0.113.10).

U-turn (internal user to the public IP):
```
set rulebase nat rules uturn-web from trust to untrust source 10.0.0.0/8 destination web-public
set rulebase nat rules uturn-web destination-translation translated-address web-internal
set rulebase nat rules uturn-web source-translation dynamic-ip-and-port interface-address interface ethernet1/6
```
The source translation forces the return path through the firewall.

Gotchas
- Using the post-NAT address in the security rule is the most common mistake; confirm with `test security-policy-match`.
- Omitting `translated-port` keeps the original port; omitting a `service` restriction translates every port.

## Verify
```
test nat-policy-match from untrust to untrust source 198.51.100.7 destination 203.0.113.10 protocol 6 destination-port 443
show session all filter destination 203.0.113.10
```
