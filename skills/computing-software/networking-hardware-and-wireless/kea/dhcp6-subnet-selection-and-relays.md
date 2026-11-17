---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-subnet-selection-and-relays
name: dhcp6-subnet-selection-and-relays
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, subnet-selection, relay, interface-id, linkaddr]
level: advanced
status: docs-checked
description: "How kea-dhcp6 selects a subnet for local and relayed clients via interface, linkaddr and interface-id; interface and interface-id are exclusive."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 subnet selection and relays
Unlike IPv4, the DHCPv6 server may have only link-local addresses, so it cannot infer which subnets are local. Set `interface` on a subnet to say it is reachable directly over that interface.

Relayed clients use two mechanisms:
1. `linkaddr` in RELAY_FORW: despite the name it holds an address, typically global, identifying the link. If it belongs to a defined subnet, that subnet is chosen.
2. `interface-id` option: the relay inserts a value identifying its receiving interface (examples range from "vlan100" to something cryptic). The server matches it against the subnet's `interface-id` and returns the option so the relay knows where to send the reply. Relay IDs must be configured to match.

```json
"subnet6": [ { "id": 1, "subnet": "2001:db8:beef::/48",
  "pools": [ { "pool": "2001:db8:beef::/48" } ],
  "interface-id": "vlan123" } ]
```

`interface` and `interface-id` are mutually exclusive: a subnet cannot be reachable both locally and via relays. Specifying both is a configuration error and the server refuses the configuration.

## Checked

2026-11-08. Read dhcp6-srv.rst (Kea ARM source, master branch) sections the interface paragraph of the subnet section and DHCPv6 Relays (partial read, those sections in full). Confirmed link-local reasoning, linkaddr, interface-id, and the exclusivity of interface and interface-id. Nothing removed.

Method: documentation only; no commands were run.
