---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-security-zones
name: pan-os-security-zones
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [security-zones, pan-os, zone-types, intrazone, interzone, zone-protection, user-id-enable]
level: practitioner
status: draft
description: "Design PAN-OS security zones by trust level and function, with intrazone and interzone defaults, and how a zone binds to interfaces."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/networking/configure-interfaces/security-zones"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: zones that reflect trust boundaries so rules stay short and meaningful.

Zone types: tap, virtual-wire, layer2, layer3, external (inter-vsys). An interface belongs to exactly one zone; a zone holds many interfaces of its own type.

```
configure
set zone trust network layer3 [ ethernet1/2 ethernet1/5 ]
set zone untrust network layer3 ethernet1/1
set zone dmz network layer3 ethernet1/6
set zone trust enable-user-identification yes
set zone untrust network zone-protection-profile ZP-EDGE
commit
```

Design rules
- Separate by trust and function (users, servers, dmz, management, guest), not by physical switch.
- Default rules: `intrazone-default` allows, `interzone-default` denies, both without logging. Add an explicit deny at the bottom to log denies: `set rulebase security rules deny-all from any to any action deny log-end yes`.
- `enable-user-identification` on the zone is required for User-ID mapping and user-based policy to apply to traffic sourced there.

Gotchas
- Same-zone traffic (even through two different interfaces) is allowed by default; add explicit intrazone deny rules if you rely on isolation between subnets that share a zone.
- Zone names are referenced by policy, NAT, QoS and PBF; check references with `show config running | match <zone>` before renaming.

## Verify
```
show zone-protection zone untrust
show interface logical
test security-policy-match from trust to untrust source 10.1.1.5 destination 198.51.100.7 destination-port 443 protocol 6
```
