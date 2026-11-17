---
id: computing-software.systems-network-administration.dns-dhcp.kea-relay-subnet-selection
name: kea-relay-subnet-selection
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, relay-subnet-selection, giaddr, shared-networks, relay-agent]
level: practitioner
status: verified
description: "Control how Kea selects a subnet for relayed requests: giaddr, relay addresses list, link-selection and subnet-selection options, shared networks."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#how-the-dhcpv4-server-selects-a-subnet-for-the-client
  - https://www.rfc-editor.org/rfc/rfc3527
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subnet selection by relay address

## Default logic (DHCPv4)
The ARM describes it by client type (it assumes client classification is not in play; classes
can alter the choice):
- Directly connected client: the subnet containing the address of the receiving interface (a
  subnet may also name its `interface`); with no matching subnet the packet is dropped.
- Renewing client that unicasts (accepted on any interface): the subnet containing `ciaddr`.
- Relayed packet (accepted on any interface): the subnet selected by `giaddr`.
- A subnet-selection option (118, RFC 3011) or a Relay Agent Information link-selection
  sub-option (option 82 sub-option 5, RFC 3527), when present, is used in selection; the
  exact precedence over `giaddr` is not spelled out in the ARM, so test it.
- When the chosen subnet belongs to a shared network, the whole shared network is selected.

## When giaddr is not inside the client subnet
Relays may use a loopback or a transit address as giaddr. Tell Kea explicitly:
```json
"subnet4": [{
  "id": 30, "subnet": "10.30.0.0/22",
  "relay": { "ip-addresses": [ "192.0.2.1", "192.0.2.2" ] },
  "pools": [ { "pool": "10.30.0.50 - 10.30.3.200" } ]
}]
```
If `relay` is given, `ip-addresses` is mandatory and takes a list. Subnets in one shared network
must be reached through the same relay address; giving them different relay addresses is a
configuration error, so set `relay` on the shared network instead. Kea picks a subnet inside the
shared network and moves to another if allocation fails (for example pool exhaustion), but do not
assume it fills the first subnet completely before using the next.

## Shared networks
Multiple subnets on one VLAN (secondary addresses):
```json
"shared-networks": [{ "name": "vlan30", "relay": { "ip-addresses": ["10.30.0.1"] },
  "subnet4": [ { "id": 30, "subnet": "10.30.0.0/24", ... }, { "id": 31, "subnet": "10.31.0.0/24", ... } ] }]
```

## Link selection
A relay that inserts the link-selection sub-option (RFC 3527) carrying the client subnet lets
`giaddr` be any reachable address; how to enable that is vendor-specific, so check the relay's
documentation. Kea honours the sub-option unless the compatibility flag is set:
```json
"compatibility": { "ignore-rai-link-selection": true }
```
The flag (default false, not RFC compliant) makes normal logic drive selection, for relays that
include wrong link-selection data and cannot be told to omit it.

## Troubleshooting
- `DHCP4_SUBNET_SELECTION_FAILED` (debug level 50) and `DHCP4_PACKET_NAK_0001` ("failed to select a
  subnet for incoming packet"): giaddr not in any subnet or relay list. For a directly connected
  client the drop message is `DHCP4_PACKET_DROP_0002` ("no suitable subnet configured for a direct
  client").
- Enable `kea-dhcp4.packets` and `kea-dhcp4.dhcpsrv` debug logging to see the selection decision.

## Verify
- [ ] Relayed clients from each VLAN get addresses from the correct subnet, with no subnet-selection failures logged.
