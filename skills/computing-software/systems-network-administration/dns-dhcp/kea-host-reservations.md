---
id: computing-software.systems-network-administration.dns-dhcp.kea-host-reservations
name: kea-host-reservations
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, kea-dhcp4, host-reservation, dhcp-reservation, hw-address, client-id, circuit-id, flex-id, reservations-out-of-pool, reservations-global, host-cmds, hosts-database]
level: practitioner
status: verified
description: "Reserve addresses in Kea: identifier types (hw-address, client-id, circuit-id, flex-id), in-pool vs out-of-pool, global vs subnet reservations, host databases and host_cmds API."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#host-reservations-in-dhcpv4
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-host-cmds-so-host-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea host reservations

## In the config file
```json
"subnet4": [{
  "id": 10, "subnet": "10.20.10.0/24",
  "pools": [{"pool": "10.20.10.100 - 10.20.10.250"}],
  "reservations": [
    {"hw-address": "00:11:22:33:44:55", "ip-address": "10.20.10.20", "hostname": "printer-2f"},
    {"client-id": "01:00:11:22:33:44:66", "ip-address": "10.20.10.21"},
    {"circuit-id": "'sw3-gi1/0/7'", "ip-address": "10.20.10.22"},
    {"hw-address": "00:11:22:33:44:77", "option-data": [{"name": "tftp-server-name", "data": "10.0.0.69"}]}
  ],
  "reservations-out-of-pool": true
}]
```
- Identifier types: `hw-address`, `client-id` (option 61, `01`+MAC for Ethernet), `duid`,
  `circuit-id` (relay option 82 sub-option 1: port-based addressing; a text value is written in
  single quotes inside the JSON string, as in the example), `flex-id` (expression via the flex_id
  hook). `host-reservation-identifiers` sets which are tried and in what order; the default is
  `hw-address, duid, circuit-id, client-id`. Keep the list short, most frequent type first: the
  search stops at the first reservation found.
- A reservation can give only options/hostname/class (no IP): the client still gets a pool address.
- **Out-of-pool** reservations (outside `pools`) are the ARM's recommended form: no other client
  can be given that address. `reservations-out-of-pool: true` (default false) tells Kea no
  reservation is inside a pool so it skips the in-pool checks and runs faster; Kea does not
  sanity-check this, so a reservation inside a pool then misbehaves. The in-pool checks are on by
  default (`reservations-in-subnet: true`).
- Global reservations (`"reservations"` at Dhcp4 level) follow a device across subnets; enable with
  `reservations-global: true` (default false). A subnet reservation beats a global one for the
  same client. The three flags can be set globally, per shared network and per subnet; setting
  all three to false disables reservations entirely.

## At scale: host database
Store reservations in MySQL/PostgreSQL (the `hosts-databases` list; the single `hosts-database`
keyword is deprecated from Kea 3.3.0), manage via the `host_cmds` hook:
```
{"command": "reservation-add", "service": ["dhcp4"],
 "arguments": {"reservation": {"subnet-id": 10, "hw-address": "00:11:22:33:44:88", "ip-address": "10.20.10.23"}}}
```
Also `reservation-get`, `reservation-del`, `reservation-update`, `reservation-get-by-hostname`,
`reservation-get-by-id`, `reservation-get-page`. No reload needed. By default the modifying
commands only target the host database (`operation-target`: `memory`, `database`, `all`); without
a writable `hosts-databases` they fail. Changes made to hosts from the JSON config are volatile
until saved with `config-write`. Use `"subnet-id": 0` for a global reservation.

## Gotchas
- Reserving an address that another client currently leases is allowed but slow to resolve: the
  reserved client is meanwhile given a temporary pool address, the old holder is NAKed at its next
  renewal, and the process takes roughly `renew-timer`. Prefer out-of-pool addresses or free the
  old lease first (`lease4-del`).
- Clients that randomise their MAC address per network break MAC reservations; reserve by
  client-id or turn randomisation off for that device.
- Two reservations for the same IP in one subnet are refused unless
  `ip-reservations-unique` is set to false (default true; supported for memfile, MySQL and
  PostgreSQL, not with Host Cache or RADIUS).

## Verify
- [ ] Reserved device receives its IP after renew (`DHCP4_LEASE_ALLOC` shows the reserved address).
- [ ] `reservation-get` returns the entry when using a host DB.
