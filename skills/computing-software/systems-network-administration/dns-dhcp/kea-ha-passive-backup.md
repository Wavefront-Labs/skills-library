---
id: computing-software.systems-network-administration.dns-dhcp.kea-ha-passive-backup
name: kea-ha-passive-backup
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [kea, dhcp-ha, passive-backup, kea-ha, lease-updates, high-availability, libdhcp-ha]
level: practitioner
status: verified
description: "Configure Kea HA passive-backup mode: one active server sending lease updates to backups, wait-backup-ack, manual promotion when the primary fails, and when to choose it."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#passive-backup-configuration
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#passive-backup-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea HA passive-backup

In passive-backup mode only the primary serves clients. It pushes every lease change to one or
more backup servers so they hold a current lease database. There is no failover: the primary sits
in the `passive-backup` state and the failure-detection parameters (`heartbeat-delay`,
`max-unacked-clients`, `max-rejected-lease-updates` and similar) must not be set. With no backup
servers it is no different from running a single server with no HA.

## When to use it
- You want lease data replicated (DR copy, another site) without the complexity of
  load-balancing/hot-standby states.
- You accept manual intervention if the primary fails, or you pair it with an external mechanism.
- A shared SQL lease database is not an option.

## Configuration (primary)
```json
"hooks-libraries": [
  { "library": "libdhcp_lease_cmds.so" },
  { "library": "libdhcp_ha.so",
    "parameters": { "high-availability": [ {
      "this-server-name": "dhcp1",
      "mode": "passive-backup",
      "wait-backup-ack": false,
      "peers": [
        { "name": "dhcp1", "url": "http://10.0.0.11:8001/", "role": "primary" },
        { "name": "dhcp2", "url": "http://10.0.0.12:8001/", "role": "backup" },
        { "name": "dhcp3", "url": "http://10.1.0.11:8001/", "role": "backup" }
      ]
    } ] } }
]
```
The ARM example shows all three peers' configs; a backup uses the same `peers` list with its own
`this-server-name`. Both lease_cmds and ha hooks are required. The HA hook can listen on its own
dedicated HTTP listener (`http-dedicated-listener`, on by default for HA multi-threading since
Kea 2.3.7 development / 2.4 stable), so no Control Agent is needed. Peer URLs must use an IP
address, not a host name, and each peer on a server needs a unique address/port pair.

- `wait-backup-ack: false` (default): primary answers clients without waiting for backups (fast;
  a backup may miss updates if it is down). Update queues grow under heavy load and Kea logs
  `HTTP_CLIENT_QUEUE_SIZE_GROWING` warnings if a queue grows too fast.
- `true` (allowed only in passive-backup mode): the primary waits for every backup's acknowledgement
  and drops the DHCP query if any lease update fails, so one dead backup stops DHCP service for
  clients and latency rises. ISC recommends leaving it false unless lease consistency matters
  more than availability.

## Failure of the primary
If the primary fails, DHCP service is lost until the administrator restarts it. The ARM also
allows configuring a backup to serve clients, since it should hold accurate or nearly accurate
leases: reconfigure that server to provide service, reload, and make sure relays send to it.
Document and test this runbook; it is the price of the simple mode.

## Verify
```
echo '{"command":"ha-heartbeat"}' | socat UNIX:/run/kea/kea4-ctrl-socket -,ignoreeof     # reports the state (passive-backup on the primary)
echo '{"command":"lease4-get-all"}' | socat UNIX:/run/kea/kea4-ctrl-socket -,ignoreeof    # compare counts on the backup
```
- [ ] Lease counts on backups track the primary, and the promotion runbook has been tested.
