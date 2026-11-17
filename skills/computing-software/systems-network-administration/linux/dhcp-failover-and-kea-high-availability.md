---
id: computing-software.systems-network-administration.linux.dhcp-failover-and-kea-high-availability
name: dhcp-failover-and-kea-high-availability
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dhcp-failover, kea-ha, kea-dhcp4, high-availability, hot-standby, load-balancing-dhcp]
level: practitioner
status: docs-checked
description: "Make DHCP highly available on Linux: Kea HA hook in load-balancing or hot-standby mode, lease sync, partner-down handling, and legacy ISC dhcpd failover peers."
sources:
  - https://github.com/isc-projects/kea/blob/master/doc/sphinx/arm/hooks-ha.rst
  - https://github.com/isc-projects/kea/blob/master/doc/sphinx/arm/ctrl-channel.rst
  - https://github.com/isc-projects/dhcp/blob/master/server/dhcpd.conf.5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DHCP failover and Kea high availability

## Kea HA (libdhcp_ha.so)
Requires the `libdhcp_lease_cmds.so` hook too. Both servers share the same subnet config; the HA hook syncs leases over the control API.
```json
"hooks-libraries": [
  { "library": "libdhcp_lease_cmds.so" },
  { "library": "libdhcp_ha.so",
    "parameters": { "high-availability": [ {
      "this-server-name": "dhcp1",
      "mode": "load-balancing",
      "heartbeat-delay": 10000,
      "max-response-delay": 60000,
      "max-ack-delay": 5000,
      "max-unacked-clients": 5,
      "multi-threading": { "enable-multi-threading": true, "http-dedicated-listener": true, "http-listener-threads": 4, "http-client-threads": 4 },
      "peers": [
        { "name": "dhcp1", "url": "http://10.0.0.2:8001/", "role": "primary" },
        { "name": "dhcp2", "url": "http://10.0.0.3:8001/", "role": "secondary" }
      ] } ] } }
]
```
- Modes: `load-balancing` (both answer; you must split the address pools between the two servers with client classification, `HA_server1`/`HA_server2`, so they never hand out the same address), `hot-standby` (`role: standby` peer answers only when the primary is down; no pool split) or `passive-backup` (one active server plus backups). Add `"role": "backup"` peers that just receive lease copies.
- `this-server-name` differs per server; everything else is identical - template it.
- Each peer `url` is the HA listener (`http-dedicated-listener`, default true); it must use a different address/port pair from the server's HTTP control socket.
- Protect the HA URL: use TLS (`trust-anchor`, `cert-file`, `key-file`, `cert-required`) as in the Kea HA TLS example.
- Active servers warn when clock skew exceeds 30 s and terminate HA (`terminated` state) above 60 s, so keep clocks in sync.

## Operating
```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"command":"ha-heartbeat"}' http://10.0.0.2:8000/
curl -s -X POST -H 'Content-Type: application/json' -d '{"command":"status-get"}' http://10.0.0.2:8000/   # HA state of both servers
```
These go to the daemon's HTTP control socket (`control-sockets` with `socket-type: http`). Kea 3.1.8 removed the Control Agent; before that the same commands went to the Control Agent with a `"service": ["dhcp4"]` field.
States: `waiting` -> `syncing` (bulk lease fetch) or `ready` -> `load-balancing`/`hot-standby`. In `load-balancing`, losing contact first gives `communication-recovery`. When the partner has been silent for `max-response-delay` the server runs failure detection (`max-ack-delay`, `max-unacked-clients`, default 10; 0 skips detection) and then enters `partner-down` to serve all clients.
Maintenance: send `ha-maintenance-start` to the server that should take over; it enters `partner-in-maintenance` and its partner enters `in-maintenance`, where it can be shut down safely.

## Legacy ISC dhcpd failover (EOL, still common)
```
failover peer "dhcp-fo" {
  primary; address 10.0.0.2; port 647; peer address 10.0.0.3; peer port 647;
  max-response-delay 60; max-unacked-updates 10; mclt 3600; split 128; load balance max seconds 3;
}
subnet 10.0.10.0 netmask 255.255.255.0 { pool { failover peer "dhcp-fo"; range 10.0.10.100 10.0.10.200; } }
```
`mclt` must be set on the primary and may not be set on the secondary; `split` and `hba` are alternatives, never both. The default failover port is the IANA port 647. To declare the other server dead, put the survivor in PARTNER-DOWN with `omshell` or by editing the last failover state in the lease file.

## Verify
- [ ] Stop dhcp1: dhcp2 enters partner-down and clients still get leases.
- [ ] `lease4-get` for a client returns the same lease on both servers.

## Checked

Checked 2026-10-26 against the Kea ARM sources in isc-projects/kea master (last commit 2026-10-21; docs describe Kea 3.x): hooks-ha.rst and ctrl-channel.rst, and ISC DHCP server/dhcpd.conf.5 (isc-projects/dhcp, final release 4.4.3-P1). Confirmed: HA modes, roles and states (including communication-recovery, in-maintenance, partner-in-maintenance, terminated), parameter defaults (max-ack-delay 10000, max-unacked-clients 10), HA+MT parameters and defaults, clock skew warn/terminate thresholds (30 s and 60 s), required lease_cmds hook, ha-maintenance-start semantics, dhcpd failover syntax (mclt primary only, port 647 default, omshell or lease-file edit for PARTNER-DOWN). Corrected: load-balancing needs a manual pool split by client class; the Control Agent was removed in Kea 3.1.8 (control commands go to the daemon HTTP socket, no service field); ha-maintenance-start was described backwards; absolute hook paths and the dhcpd clock-sync claim were removed.

Method: documentation only; no commands were run.
