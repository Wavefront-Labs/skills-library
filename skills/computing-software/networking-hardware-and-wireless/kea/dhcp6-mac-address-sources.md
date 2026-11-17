---
id: computing-software.networking-hardware-and-wireless.kea.dhcp6-mac-address-sources
name: dhcp6-mac-address-sources
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp6, mac-sources, hardware-address, duid, rfc6939]
level: advanced
status: docs-checked
description: "Control how kea-dhcp6 finds client MAC addresses with mac-sources: any, duid, ipv6-link-local, remote-id, docsis and more."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv6 MAC address sources
DHCPv6 has no fully reliable way to obtain a client MAC address. The global `mac-sources` list picks methods and their order; it must have at least one value. When unset it is "any": try every method in sequence and use the first that succeeds. The docs say "any" suffices in a typical deployment.

Methods:
- `any`: keyword, try all.
- `raw`: not implemented for DHCPv6; no effect.
- `duid`: parse DUID-LLT (default) or DUID-LL for a MAC. RFC 9915 forbids this, and clients may use DUID-EN or DUID-UUID, so it is unreliable.
- `ipv6-link-local`: derive from an EUI-64 source link-local address (u-bit 1, g-bit 0). Fails with privacy extensions (RFC 4941).
- `client-link-addr-option` (alias `rfc6939`): option inserted by a relay; useless for directly connected clients.
- `remote-id` (alias `rfc4649`): relay-inserted; may carry the MAC depending on relay configuration.
- `subscriber-id` (alias `rfc4580`): not implemented.
- `docsis-cmts`: for cable networks where the CMTS is the relay; takes the MAC from sub-option 1026 (cm mac) of the vendor-specific option with vendor-id 4491 in the Relay-forward message.
- `docsis-modem`: takes the MAC from sub-option 36 (device-id) of the vendor-specific option with vendor-id 4491 in the original client message, not the relay options.

```json
"Dhcp6": { "mac-sources": [ "method1", "method2" ] }
```

## Checked

2026-11-08. Read dhcp6-srv.rst (Kea ARM source, master branch) sections DHCPv6 MAC/Hardware Addresses (mac-sources) in full. Confirmed all listed methods, aliases, the any default and the at-least-one-value rule. Added the documented docsis-modem method (sub-option 36 device-id, vendor-id 4491, from the client message).

Method: documentation only; no commands were run.
