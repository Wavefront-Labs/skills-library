---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-subnet-selection-and-relays
name: dhcp4-subnet-selection-and-relays
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, subnet-selection, relay, giaddr, relay-addresses]
level: advanced
status: docs-checked
description: "How kea-dhcp4 picks a subnet for local, unicast-renewing and relayed clients, and how to bind a subnet to a relay address."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 subnet selection and relays
Directly connected clients: the server checks the configuration for the receiving interface; if no subnet matches, the message is discarded. Set `interface` in a subnet to mark it as local to that interface. The server then processes such messages only if the interface address belongs to a configured subnet (for example 192.0.2.3 in 192.0.2.0/24).

Unicast messages (clients renewing) are accepted through any interface.

Relayed clients: normally the giaddr inserted by the relay selects the subnet. When the relay address does not match the subnet (long-running renumbering, cable networks, where modems and devices share a link but use different addressing) add the relay's address to the subnet:

```json
"subnet4": [ { "id": 1, "subnet": "192.0.2.0/24",
  "relay": { "ip-addresses": [ "10.0.0.1" ] } } ]
```

With this the subnet is selected for relays in 192.0.2.0/24 and for the relay at 10.0.0.1.

The compatibility flag `ignore-rai-link-selection` (default false, not RFC-compliant) stops the Link Selection sub-option of Relay Agent Information from driving subnet selection, helping when a relay cannot be configured to omit it and includes incorrect Link Selection data.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections How the DHCPv4 Server Selects a Subnet, Using a Specific Relay Agent for a Subnet and Ignore RAI Link Selection (partial read, those sections in full). Confirmed the interface, unicast and relay rules and the 10.0.0.1 example. Reworded the ignore-rai-link-selection use case to match the docs (relays that cannot be told which sub-options to include and send wrong Link Selection data).

Method: documentation only; no commands were run.
