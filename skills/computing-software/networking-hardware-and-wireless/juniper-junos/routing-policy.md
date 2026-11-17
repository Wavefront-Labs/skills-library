---
id: computing-software.networking-hardware-and-wireless.juniper-junos.routing-policy
name: routing-policy
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, policy-options, policy-statement, routing-policy, prefix-list]
level: practitioner
status: draft
description: "Write Junos policy-statements with terms, from/then, prefix-lists, communities and default actions for import and export."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routing policy with policy-options
Goal: control what routes are accepted and advertised.

```
set policy-options prefix-list CUST-NETS 192.0.2.0/24
set policy-options community NO-EXPORT members no-export
set policy-options policy-statement EXPORT-STATIC term 1 from protocol static
set policy-options policy-statement EXPORT-STATIC term 1 from prefix-list CUST-NETS
set policy-options policy-statement EXPORT-STATIC term 1 then accept
set policy-options policy-statement EXPORT-STATIC term DEFAULT then reject
set protocols ospf export EXPORT-STATIC
```

- Evaluation: terms top-down; first term whose `from` matches runs its `then`; `accept`/`reject` end evaluation; no action continues.
- Default action depends on protocol: BGP import accepts, BGP export advertises only BGP-learned active routes, OSPF export none (confirm per protocol).
- Chain with `export [ A B C ]`; `next policy` skips to the next policy.

Gotcha: a policy with no final `reject` term falls to the protocol default, often exporting more than intended. End export policies with an explicit catch-all term.

## Verify
- `show route advertising-protocol bgp <peer>` or `show ospf database external` shows only intended prefixes.
- `test policy EXPORT-STATIC 192.0.2.0/24` returns the prefix as accepted.
