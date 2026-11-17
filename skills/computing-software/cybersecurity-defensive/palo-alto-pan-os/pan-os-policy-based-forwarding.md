---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-policy-based-forwarding
name: pan-os-policy-based-forwarding
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [policy-based-forwarding, pan-os, pbf, egress-interface, symmetric-return, forwarding-rule]
level: practitioner
status: draft
description: "Write PAN-OS policy based forwarding rules to steer traffic out a chosen ISP, with monitoring failover and symmetric return."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/policy/policy-based-forwarding"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: send selected traffic (by source, app or service) out a specific interface or next hop, overriding the routing table.

```
configure
set rulebase pbf rules guest-via-isp2 from zone guest source 10.30.0.0/24 destination any application any service any
set rulebase pbf rules guest-via-isp2 action forward egress-interface ethernet1/3 nexthop ip-address 198.51.100.1
set rulebase pbf rules guest-via-isp2 action forward monitor profile failover ip-address 198.51.100.1
set rulebase pbf rules guest-via-isp2 enforce-symmetric-return enabled yes nexthop-address-list 198.51.100.1
commit
```
The monitor profile `failover` stops using the rule when the next hop is unreachable and falls back to normal routing; `wait-recover` waits for recovery before resuming.

Key facts
- PBF is evaluated on the first packet of a session, before route lookup, and the decision sticks for the session.
- PBF matches the source zone or interface only, not the destination zone.
- App-ID is not known on the first packet, so use service or address criteria for reliability.

Gotchas
- Return traffic follows the routing table unless symmetric return is on; asymmetric paths break stateful inspection.
- NAT must match the egress interface chosen by PBF.

## Verify
```
test pbf-policy-match from zone guest source 10.30.0.10 destination 198.51.100.7 protocol 6 destination-port 443
show session all filter source 10.30.0.10
```
The session's egress interface should be ethernet1/3.
