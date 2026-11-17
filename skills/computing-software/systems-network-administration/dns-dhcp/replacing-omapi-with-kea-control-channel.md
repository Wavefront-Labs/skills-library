---
id: computing-software.systems-network-administration.dns-dhcp.replacing-omapi-with-kea-control-channel
name: replacing-omapi-with-kea-control-channel
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, omapi, omshell, control-agent, isc-dhcp-migration]
level: practitioner
status: verified
description: "Replace ISC dhcpd OMAPI/omshell automation with Kea's control channel: host_cmds and lease_cmds via REST, authentication and script conversion."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-host-cmds-so-host-commands
  - https://kb.isc.org/docs/isc-dhcp-44-manual-pages-omshell
  - https://github.com/isc-projects/dhcp/blob/master/dhcpctl/omshell.1
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Replacing OMAPI with the control channel

dhcpd tools (omshell scripts, other OMAPI clients, IPAM integrations) used OMAPI (omshell's default
port is 7911) to add hosts and look up leases at runtime. Kea has no OMAPI; it uses JSON commands.
Hosts created through OMAPI were saved in dhcpd.leases, and keama does not convert them, so
recreate them as reservations (ISC's KB article on the migration assistant says the same).

## Mapping
| OMAPI action | Kea |
|--------------|-----|
| `new host; set hardware-address; set ip-address; create` | `reservation-add` (host_cmds hook, needs host DB backend for persistence) |
| `open host` / remove | `reservation-get`, `reservation-del` |
| `new lease; set ip-address; open` | `lease4-get` with `"address"` (lease_cmds) |
| lease release via OMAPI | `lease4-del` |
| OMAPI key (TSIG-style key; omshell's default algorithm is HMAC-MD5, with HMAC-SHA1 to SHA512 selectable) | HTTP control socket basic authentication and/or TLS client certificates (via the Control Agent on Kea 3.0.x and earlier) |

## Setup
```json
"hooks-libraries": [
  { "library": "libdhcp_host_cmds.so" },
  { "library": "libdhcp_lease_cmds.so" }
],
"hosts-databases": [ { "type": "postgresql", "name": "kea", "user": "kea", "password": "..." } ]
```
`hosts-databases` is a list; the older single `hosts-database` keyword is deprecated from Kea 3.3.0.
`reservation-add`, `reservation-del` and `reservation-update` target the host database by default
(`operation-target` can select `memory`, `database` or `all`), and fail if no writable database
is configured. Changes made to hosts held in the JSON config are volatile until `config-write`
saves them.

## Script conversion example
omshell:
```
server localhost
key omapi_key <secret>
connect
new host
set name = "printer7"
set hardware-address = 00:11:22:33:44:55
set ip-address = 10.0.5.7
set hardware-type = 1
create
```
Kea:
```
curl -su admin:$PASS -X POST https://kea1:8000/ -H 'Content-Type: application/json' -d '{
 "command": "reservation-add",
 "arguments": { "reservation": { "subnet-id": 5, "hw-address": "00:11:22:33:44:55",
   "ip-address": "10.0.5.7", "hostname": "printer7" } } }'
```
Add `"service": ["dhcp4"]` when the request goes through a Control Agent (Kea 3.0.x and earlier).
Note the subnet ID requirement: a reservation belongs to a subnet by `subnet-id` (0 means a global
reservation, which also needs `reservations-global: true`). Only `subnet-id` and one identifier
are mandatory.

## Verify
- [ ] The converted automation creates and deletes reservations visible in `reservation-get`, and they survive a Kea restart.
