---
id: computing-software.systems-network-administration.dns-dhcp.kea-lease-cmds-hook
name: kea-lease-cmds-hook
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, lease-cmds, lease-api, control-agent, rest-api]
level: practitioner
status: verified
description: "Manage individual Kea leases through the lease_cmds hook: get, add, update, delete and wipe leases, query by MAC or hostname, and safe automation patterns."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-lease-cmds-so-lease-commands-for-easier-lease-management
  - https://kea.readthedocs.io/en/latest/api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lease_cmds hook

## Load
```json
"hooks-libraries": [ { "library": "libdhcp_lease_cmds.so" } ]
```
Required by HA too. Commands reach Kea via the unix control socket or an HTTP control socket (default
port 8000; through the Control Agent on Kea 3.0.x and earlier, which then also needs `"service": ["dhcp4"]`).

## Common commands
```
curl -s -X POST http://127.0.0.1:8000/ -H 'Content-Type: application/json' -d '{
  "command": "lease4-get-by-hw-address",
  "arguments": { "hw-address": "aa:bb:cc:dd:ee:ff" } }'
```
| Command | Use |
|---------|-----|
| `lease4-get` | by `address`, or `subnet-id`+`identifier-type`+`identifier` |
| `lease4-get-by-hw-address` / `-by-client-id` / `-by-hostname` / `-by-state` | find a client or leases in a state |
| `lease4-get-all` / `lease4-get-page` | dump (paged for large tables: `"from": "start", "limit": 1000`) |
| `lease4-add` | insert a lease (needs `ip-address` and `hw-address`; `subnet-id` optional, found by subnet selection when omitted or 0) |
| `lease4-update` | change any field except the address (use del + add to change that) |
| `lease4-del` | free an address (client moved, conflict) |
| `lease4-wipe` | remove all leases of one subnet when it is retired; no DNS updates, log messages or hook calls |
| `lease4-resend-ddns` | re-send the DNS update request for a lease |
| `lease4-write` | memfile only: write the in-memory leases to a CSV file for recovery |
DHCPv6 equivalents use `lease6-*` with `duid` and `iaid` (plus `lease6-bulk-apply`).

## Automation patterns
- Decommission: `lease4-del` by IP when a host is retired so the address returns immediately.
- IPAM sync: page through `lease4-get-page` periodically (see lease-sync) instead of reading the CSV.
- Fixing conflicts: delete the declined/conflicting lease after removing the static device.

## Cautions
- `lease4-add` on an address in a pool does not tell the client anything; it only reserves server-side.
- Deleting an active lease lets the server reassign the address while the client still uses it until
  it renews; prefer short lease times when moving clients.
- Results return `"result": 3` (empty) when nothing matched, `1` for an error such as a missing
  parameter; handle both in scripts.

## Verify
- [ ] `lease4-get` returns the expected lease after add/update and `"result": 3` after delete.
