---
id: computing-software.systems-network-administration.dns-dhcp.kea-ha-maintenance-mode
name: kea-ha-maintenance-mode
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, ha-maintenance, high-availability, kea-ha, planned-maintenance]
level: practitioner
status: verified
description: "Take a Kea HA partner down for planned maintenance with ha-maintenance-start/cancel so the other server serves all clients without lease loss."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#controlled-shutdown-and-maintenance-of-dhcp-servers
  - https://kea.readthedocs.io/en/latest/api.html#ha-maintenance-start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HA maintenance mode

Stopping an HA partner abruptly makes the survivor wait (`max-response-delay`, then the
unacked-client test governed by `max-ack-delay` and `max-unacked-clients`) before going
partner-down, causing a gap in service. Maintenance mode hands over immediately.

## Procedure
1. On the server that will STAY up, send:
```
{ "command": "ha-maintenance-start", "service": ["dhcp4"] }
```
The server sends `ha-maintenance-notify` to the peer; if the peer confirms, the sender moves to
`partner-in-maintenance` and the peer to `in-maintenance`. The surviving server serves all scopes
and keeps sending lease updates; the peer stops answering clients. The command returns an error if
the states do not allow it (for example the peer is a backup server, the server is `terminated`,
or the command was already sent to the other server).
2. Confirm: `status-get` shows the states. Then stop and patch the peer (Kea upgrade, OS reboot).
   Once the peer stops responding the survivor drops to `partner-down` and stops sending updates.
3. Start the peer. State negotiation and lease synchronisation (`syncing`, `ready`) run, and both
   servers return to `load-balancing` / `hot-standby` automatically.
4. If you abandon maintenance before stopping the peer: send `ha-maintenance-cancel` to the server
   in `partner-in-maintenance`. Once it has moved on to `partner-down` it is too late to cancel:
   restart the other server and let normal state negotiation finish.

With several relationships (hub-and-spoke), `ha-maintenance-start` tries to move all of them to
`partner-in-maintenance` and returns an error if any partner fails; `ha-maintenance-cancel`
resumes normal operation.

## Upgrade notes
- Upgrade one partner at a time while the other serves everything; then repeat for the second
  (send `ha-maintenance-start` to the one that is staying up each time).
- Read the release notes of the versions involved before mixing Kea versions in a pair.
- Lease backends: back up memfile CSV/DB before upgrades.

## Watch
```
tail -f /var/log/kea/kea-dhcp4.log | grep -E 'HA_|STATE'
```
Messages like `HA_STATE_TRANSITION ... partner-in-maintenance` confirm the handover.

## Verify
- [ ] During maintenance, new clients get leases from the surviving server, and after restart both servers return to normal state with synced lease counts.
