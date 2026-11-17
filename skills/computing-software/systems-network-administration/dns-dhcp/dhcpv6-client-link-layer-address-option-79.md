---
id: computing-software.systems-network-administration.dns-dhcp.dhcpv6-client-link-layer-address-option-79
name: dhcpv6-client-link-layer-address-option-79
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcpv6, option-79, client-link-layer-address, relay-agent, kea]
level: practitioner
status: verified
description: "Recover client MAC addresses for DHCPv6 via relay option 79 (RFC 6939), enable it on relays, and use it in Kea reservations and logging."
sources:
  - https://www.rfc-editor.org/rfc/rfc6939
  - https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html#mac-addresses-in-dhcpv6
  - https://www.rfc-editor.org/rfc/rfc9915
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client link-layer address option 79

DHCPv6 identifies clients by DUID, not MAC. Operators who track devices or reserve addresses by
MAC need the hardware address. RFC 6939 lets the first-hop relay insert option 79
(client link-layer address) in Relay-Forw messages.

## Relay config
The relay must be configured to insert option 79; the syntax is vendor-specific, so use the relay
vendor's documentation. The Kea ARM notes that this method needs a relay agent that supports the
option and is configured to insert it, and that it is useless for directly connected clients.

## Kea MAC sources
Kea can derive a MAC from several places; `mac-sources` sets which methods to use and in what order,
and the default `any` tries every method in turn and uses the first that succeeds:
```json
"mac-sources": [ "client-link-addr-option", "duid", "ipv6-link-local", "remote-id", "docsis-cmts" ]
```
`subscriber-id` is also accepted but the Kea ARM says it is not implemented; `docsis-modem` and `raw`
(no effect for DHCPv6) also exist.
- `client-link-addr-option` = option 79 (alias `rfc6939`), the option a relay inserts.
- `duid` works for DUID-LL/LLT types (contains MAC), not DUID-EN/UUID.
- `ipv6-link-local` only for directly connected clients using EUI-64 link-local addresses.

## Reservations by MAC
```json
"reservations": [ { "hw-address": "aa:bb:cc:dd:ee:ff", "ip-addresses": ["2001:db8:1::50"] } ],
"host-reservation-identifiers": [ "hw-address", "duid" ]
```

## Wireshark
`dhcpv6.option.type == 79` inside the relay message; the decoded address is in
`dhcpv6.client_link_layer_addr_ether` (or `dhcpv6.client_link_layer_addr`), field names from Wireshark 4.4.1.

## Verify
- [ ] Kea leases for relayed clients are found by MAC (the lease_cmds hook provides `lease6-get-by-hw-address`) and MAC reservations match.
