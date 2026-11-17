---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-rapid-commit-and-stateless-mode
name: dhcp6-rapid-commit-and-stateless-mode
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, rapid-commit, stateless, information-request]
level: practitioner
status: docs-checked
description: "Enable DHCPv6 Rapid Commit per subnet and serve options-only clients (INFORMATION-REQUEST) from kea-dhcp6."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 Rapid Commit and stateless mode
Rapid Commit (RFC 9915) is supported but disabled by default. Enable it per subnet:

```json
"subnet6": [ { "id": 1, "subnet": "2001:db8:beef::/48",
  "rapid-commit": true,
  "pools": [ { "pool": "2001:db8:beef::1-2001:db8:beef::10" } ] } ]
```

It affects only that subnet. For clients on other subnets the server ignores the Rapid Commit option and follows the 4-message exchange, answering a Solicit that contains Rapid Commit with an Advertise.

Stateless mode: clients send INFORMATION-REQUEST to get options only. The server answers with requested options it has, trying per-subnet options first and then global ones. No special configuration is needed, and stateless and stateful clients can be served together; stateful configuration simply gives stateless clients only the options they asked for. A server can provide options and no addresses or prefixes; if the options are the same in every subnet, define them globally and omit subnets.

## Checked

2026-11-08. Read dhcp6-srv.rst (Kea ARM source, master branch) sections Rapid Commit and Stateless DHCPv6 (INFORMATION-REQUEST Message) (partial read, those sections in full). Confirmed per-subnet enablement, default off, behaviour on other subnets, option lookup order and the options-only server. Nothing removed.

Method: documentation only; no commands were run.
