---
id: computing-software.systems-network-administration.dns-dhcp.kea-lease-backends-and-control-agent
name: kea-lease-backends-and-control-agent
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, lease-database, memfile, mysql, postgresql, kea-lfc, kea-ctrl-agent, kea-api, control-socket, config-get, config-reload, config-test, keactrl, rest-api]
level: practitioner
status: verified
description: "Choose Kea lease storage (memfile with LFC vs MySQL/PostgreSQL) and manage Kea via control socket and REST agent: config-test/reload, lease queries, API security."
sources:
  - https://kea.readthedocs.io/en/latest/arm/admin.html
  - https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kea lease backends and the control agent

## Lease storage
| Backend | Use | Notes |
|---|---|---|
| memfile (CSV) | default; fastest; single server or HA pairs | `kea-lfc` periodically compacts the CSV (`lfc-interval` seconds, default 3600, 0 disables) |
| MySQL / PostgreSQL | shared visibility, reporting, large estates | `kea-admin db-init mysql -u kea -p ... -n kea` creates schema; `kea-admin db-upgrade` after Kea upgrades |
```json
"lease-database": {"type": "memfile", "persist": true, "name": "kea-leases4.csv", "lfc-interval": 3600}
"lease-database": {"type": "postgresql", "name": "kea", "host": "db1", "user": "kea", "password": "<DB_PASS>"}
```
Since Kea 2.7.9 a memfile lease file must live in the build-time data directory
(`var/lib/kea` under the install prefix) or the one named by `KEA_DHCP_DATA_DIR`; a `name` with
any other path is refused, so give a bare file name to use the default directory.

HA (hook) works with memfile: each server keeps its own copy and syncs via the HA protocol; a
shared database is **not** required. With a database that replicates itself, HA lease updates and
sync can be switched off (`send-lease-updates` and `sync-leases` false); see the shared-database
skill.

## Control socket (local)
```json
"control-sockets": [{"socket-type": "unix", "socket-name": "/run/kea/kea4-ctrl-socket"}]
```
```
echo '{"command": "config-get"}' | socat UNIX:/run/kea/kea4-ctrl-socket -,ignoreeof
```
`control-sockets` is a list since Kea 2.7.2 (the single `control-socket` map is accepted from 2.7.2 to
3.3.0 and deprecated from 3.3.1). Since 2.7.9 the socket must be in the build-time run directory or
`KEA_CONTROL_SOCKET_DIR`, which must have 0750 permissions; only one `unix` entry is allowed.

## HTTP/HTTPS control (REST, default port 8000)
Since Kea 2.7.2 the DHCP servers and D2 serve HTTP/HTTPS themselves from the same list (several
connections since 2.7.6). This replaces the Control Agent, which was removed in Kea 3.1.8
(development), so it is absent from the 3.2 stable series but still present in 3.0.x:
```json
"control-sockets": [{"socket-type": "https", "socket-address": "10.20.30.40", "socket-port": 8004,
  "trust-anchor": "/path/ca.pem", "cert-file": "/path/cert.pem", "key-file": "/path/key.pem",
  "cert-required": true,
  "authentication": {"type": "basic", "directory": "/etc/kea", "clients": [{"user": "admin", "password-file": "admin.pw"}]}}]
```
`socket-address` defaults to 127.0.0.1 and `socket-port` to 8000, and two servers (and HA
listeners) must not share an address/port pair. Keep it on localhost or a management interface and
use basic auth plus TLS. On Kea 3.0.x with the Control Agent, the equivalent is a `Control-agent`
section with `http-host`, `http-port`, `authentication` and `control-sockets` keyed by service
name (`dhcp4`), and requests carry `"service": ["dhcp4"]`.

## Safe config changes
```
curl -s -u admin:<PW> -X POST http://127.0.0.1:8000/ -H 'Content-Type: application/json' \
  -d '{"command":"config-test","arguments":{"Dhcp4": {...}}}'
curl ... -d '{"command":"config-reload"}'       # re-read the file on disk
curl ... -d '{"command":"config-write"}'        # save running (after config-set)
curl ... -d '{"command":"lease4-get","arguments":{"address":"10.20.10.57"}}'
```
Add `"service":["dhcp4"]` to each request when going through a Control Agent.
`kea-dhcp4 -t /etc/kea/kea-dhcp4.conf` validates offline (`-T` also opens databases and loads hooks).
`keactrl status` (or systemd units) for daemon state. `lease4-get` needs the lease_cmds hook and takes
`address` (or `subnet-id`, `identifier-type`, `identifier`), not `ip-address`.

## Verify
- [ ] Lease file/DB grows with allocations; LFC runs (`kea-leases4.csv.2` is the LFC input, then
  `.1`, `.output` and `.completed` files appear, per the memfile source).
- [ ] API reachable only from management hosts with auth; config-test catches a deliberate error.
