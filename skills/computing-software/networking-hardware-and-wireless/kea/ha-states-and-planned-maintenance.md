---
id: computing-software.networking-hardware-and-wireless.kea.ha-states-and-planned-maintenance
name: ha-states-and-planned-maintenance
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, high-availability, ha-maintenance-start, partner-down, ha-heartbeat]
level: advanced
status: docs-checked
description: "Understand Kea HA server states (load-balancing, communication-recovery, partner-down, in-maintenance) and take a server offline with ha-maintenance-start."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea HA states and planned maintenance
Peers query each other's state with `ha-heartbeat` over the RESTful API. If the partner does not answer in time, the server may apply additional checks, then move to partner-down and handle all traffic. It keeps sending heartbeats; when the partner returns, it synchronizes leases and the pair returns to the normal state.

Selected states:
- `load-balancing` / `hot-standby`: normal operation for each mode.
- `communication-recovery`: load-balancing servers go here on control channel trouble (since 1.9.4), still answering clients but queuing lease updates; `delayed-updates-limit` (default 100, load-balancing mode only) set to 0 disables the state. Before 1.9.4 they went straight to partner-down.
- `partner-down`: partner detected offline; this server answers all queries. Not entered if only a backup server is down.
- `in-maintenance`: set by the partner's request; safe to shut down.
- `partner-in-maintenance`: set on the server that received `ha-maintenance-start`; it answers all queries and keeps sending lease updates to the partner until the partner stops responding.
- `terminated`: the HA library cannot provide reliable service and manual intervention is needed; the server keeps answering clients in the selected mode but exchanges no lease updates or heartbeats, and stays there until restarted or its configuration is reloaded.
- `backup`: normal for backup servers, receiving updates.

Maintenance gives direct control: sending `ha-maintenance-start` to server1 makes it tell server2 (`ha-maintenance-notify`) to enter in-maintenance. Once confirmed, server1 enters partner-in-maintenance, keeps sending lease updates, and answers all clients. Shut server2 down; server1 then moves to partner-down. Restarting server2 triggers state negotiation and synchronization. `ha-maintenance-cancel` on the server in partner-in-maintenance reverts both, but not once partner-down is reached. Maintenance returns an error for backup servers and for servers in the terminated state, or if the request was already sent to the other server.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM High Availability chapter (Server States, Controlled Shutdown and Maintenance of DHCP Servers). Removed the `down` state, which the states list on the page does not contain. Added partner-in-maintenance, terminated and the delayed-updates-limit default from the same chapter.
