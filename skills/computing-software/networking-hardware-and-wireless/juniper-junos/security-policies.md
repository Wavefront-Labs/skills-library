---
id: computing-software.networking-hardware-and-wireless.juniper-junos.security-policies
name: security-policies
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, security-policies, srx-policy, from-zone, to-zone]
level: practitioner
status: draft
description: "Write SRX from-zone/to-zone policies with applications, logging and ordering, and check session hits."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SRX security policies
Goal: control inter-zone traffic.

```
set security policies from-zone trust to-zone untrust policy ALLOW-WEB match source-address any
set security policies from-zone trust to-zone untrust policy ALLOW-WEB match destination-address any
set security policies from-zone trust to-zone untrust policy ALLOW-WEB match application [ junos-http junos-https ]
set security policies from-zone trust to-zone untrust policy ALLOW-WEB then permit
set security policies from-zone trust to-zone untrust policy ALLOW-WEB then log session-close
insert security policies from-zone trust to-zone untrust policy ALLOW-WEB before policy DENY-ALL
```

```
user@host> show security policies hit-count
user@host> show security flow session destination-prefix 203.0.113.10
```

- Policies are evaluated in order; first match wins; unmatched traffic hits the default deny.
- Global policies (`security policies global`) apply across zones and are evaluated after zone-pair policies.
- Create address-book entries under `security address-book`.

Gotcha: policy ordering mistakes (a broad permit above a specific deny). Use `insert` to reorder. Application and `application-services` (UTM/IDP) options vary by release: confirm.

## Verify
- `show security policies hit-count` counters increment; `show security flow session` lists the flow.
