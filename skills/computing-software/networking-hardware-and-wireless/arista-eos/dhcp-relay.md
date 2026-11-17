---
id: computing-software.networking-hardware-and-wireless.arista-eos.dhcp-relay
name: dhcp-relay
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, dhcp-relay, ip-helper, dhcp-server]
level: practitioner
status: draft
description: "Relay DHCP requests with ip helper-address on SVIs and DHCP server with option 82."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DHCP relay
Goal: serve DHCP from a central server.

```
interface Vlan100
   ip helper-address 192.0.2.30 source-interface Loopback0
dhcp relay
   always-on
   tunnel requests disabled
```

```
show ip dhcp relay counters
show dhcp relay
```

- `ip helper-address vrf X` for cross-VRF servers.
- Option 82 info insertion: `dhcp relay all-subnets` (confirm).
- With anycast gateways use `source-interface` to a unique loopback so the server can reply.

Gotcha: relay with a virtual (anycast) gateway address as source breaks reply routing. Use a unique per-leaf source.

Operational tip: confirm the DHCP server has a scope matching the relay gateway address (giaddr), since a missing scope looks like relay failure although the packets arrive. Use `show ip dhcp relay counters` on both the ingress and the uplink interface to see whether requests are forwarded and replies come back. Check that the relay interface has a route back to the DHCP server in the right VRF, otherwise offers never return.

## Verify
- `show ip dhcp relay counters` increases and the client receives an address.
