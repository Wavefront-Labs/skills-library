---
id: computing-software.systems-network-administration.dns-dhcp.kea-ha-state-machine
name: kea-ha-state-machine
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, dhcp-ha, dhcp-failover, kea-ha, hot-standby, load-balancing, partner-down, ha-heartbeat, ha-sync, max-unacked-clients, ha-maintenance-start, libdhcp-ha]
level: advanced
status: verified
description: "Operate Kea high availability: load-balancing vs hot-standby, the HA states (syncing, ready, partner-down, waiting), failure detection tuning, maintenance mode and recovery."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-ha-so-high-availability-outage-resilience-for-kea-servers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea HA state machine

## Modes
- **load-balancing**: both servers serve, each answering about half of the queries (RFC 3074 style
  scopes `HA_server1` and `HA_server2`; pools must be split between them, see below). Each lease
  change is sent to the partner; if the partner cannot be reached the query is dropped (see
  communication-recovery below).
- **hot-standby**: primary serves (scope `HA_server1` only), standby only syncs and takes over on
  failure.
- **passive-backup**: one primary, backups receive lease updates only, no failover (see the
  passive-backup skill). Optional **backup** servers can also be added to the other modes.

## Config core
```json
"hooks-libraries": [{"library": "/usr/lib/kea/hooks/libdhcp_lease_cmds.so"},
 {"library": "/usr/lib/kea/hooks/libdhcp_ha.so", "parameters": {"high-availability": [{
   "this-server-name": "dhcp1", "mode": "load-balancing",
   "heartbeat-delay": 10000, "max-response-delay": 60000, "max-ack-delay": 5000, "max-unacked-clients": 5,
   "peers": [{"name": "dhcp1", "url": "http://10.0.0.67:8001/", "role": "primary"},
             {"name": "dhcp2", "url": "http://10.0.0.68:8001/", "role": "secondary"}]}]}}]
```
Both servers need the same subnets and the lease_cmds hook. In load-balancing mode the ARM requires
splitting the address pools between the two servers with client classification (pool
`client-classes` of the built-in `HA_server1` and `HA_server2` classes, which the HA hook assigns
per packet), so both servers cannot hand out the same address to different clients; hot-standby
needs no split. Clients' requests must reach both servers (for example a relay with both helper
addresses).

## States
| State | DHCP service | Meaning |
|---|---|---|
| waiting | disabled | each started server enters it; waits for partner/sync decision |
| syncing | disabled | pulling leases from the partner (skipped when `sync-leases` is false) |
| ready | disabled | synced, waiting for the partner to return to normal operation |
| load-balancing / hot-standby | enabled | normal operation |
| communication-recovery | enabled | load-balancing only: partner unreachable, lease updates queued; between load-balancing and partner-down |
| partner-down | enabled, all scopes | this server serves all clients (partner considered down) |
| terminated | enabled, as normal | clock skew over 60 s or another unrecoverable problem: no lease updates or heartbeats, manual intervention |
| in-maintenance | disabled | the server about to be shut down |
| partner-in-maintenance | enabled, all scopes | the server staying up during maintenance |
| backup | n/a | backup server receiving lease updates; passive-backup is the primary's state in that mode |

## Failure detection
Communication is declared interrupted after `max-response-delay` ms without a successful exchange
(default 60000; heartbeats every `heartbeat-delay`, default 10000). Then, with a non-zero
`max-unacked-clients` (default 10), a server goes **partner-down** only when it also sees more
than that many "unacked" clients: clients whose `secs` field (DHCPv4) or elapsed-time option
(DHCPv6) exceeds `max-ack-delay` ms (default 10000). This avoids both servers going partner-down
when only the HA link fails; in load-balancing mode both servers first enter
`communication-recovery`. With `max-unacked-clients: 0` the failure-detection step is skipped and
loss of communication alone triggers partner-down (faster, but both servers may then serve the
same addresses). Setting `delayed-updates-limit` to 0 stops a server entering
`communication-recovery`.

## Operations
```
{"command": "ha-heartbeat", "service": ["dhcp4"]}           // state, scopes and unsent-update-count of the server that receives it
{"command": "status-get", "service": ["dhcp4"]}
{"command": "ha-maintenance-start", "service": ["dhcp4"]}   // send to the server staying up; partner goes to in-maintenance
{"command": "ha-maintenance-cancel", "service": ["dhcp4"]}
{"command": "ha-sync", "service": ["dhcp4"], "arguments": {"server-name": "dhcp2"}}
```
Patch one node at a time with maintenance mode so the other moves to partner-down cleanly.
NTP on both: a warning is logged above 30 s of skew, and above 60 s the HA service on both
servers terminates (they keep answering clients but stop exchanging updates, so the lease
databases diverge). After fixing the clocks restart both servers.

## Verify
- [ ] Both servers in load-balancing (or hot-standby) state per `ha-heartbeat`.
- [ ] Stopping one moves the other to partner-down after the expected detection time (log message
  `HA_STATE_TRANSITION`); restarting resyncs.
