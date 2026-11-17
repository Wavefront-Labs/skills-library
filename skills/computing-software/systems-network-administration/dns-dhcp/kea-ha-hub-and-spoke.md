---
id: computing-software.systems-network-administration.dns-dhcp.kea-ha-hub-and-spoke
name: kea-ha-hub-and-spoke
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, kea, ha-hub-and-spoke, high-availability, kea-ha, central-backup]
level: practitioner
status: verified
description: "Build a Kea HA hub-and-spoke topology (Kea 2.4+): one central server as backup partner for many branch servers with multiple HA relationships."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#hub-and-spoke-configuration
  - https://kea.readthedocs.io/en/latest/arm/hooks.html#libdhcp-ha-so-high-availability-outage-resilience-for-kea-servers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hub-and-spoke HA relationships

Support for hub-and-spoke was added in Kea 2.5.5 (development), so it is in stable releases from
2.6.0. A central "hub" can participate in several relationships, each pairing it with one branch
"spoke" in `hot-standby` mode with the branch as primary and the hub as standby. Each
relationship has its own state machine. If a branch fails, the hub takes over that branch's
traffic only (its relationship goes `partner-down`, the others stay in `hot-standby`).

## Spoke (branch) config
```json
"high-availability": [{
  "this-server-name": "branch1",
  "mode": "hot-standby",
  "peers": [
    { "name": "branch1", "url": "http://10.1.0.10:8001/", "role": "primary" },
    { "name": "hub-b1",  "url": "http://10.0.0.10:8001/", "role": "standby" }
  ]
}]
```
On the hub, each subnet carries `"user-context": { "ha-server-name": "branch1" }` (any peer name of
the relationship works) so the HA hook knows which relationship the subnet belongs to. On a
branch server it is optional if the branch only has its own subnets, but recommended: without it
the branch inserts all leases fetched from the hub, including other relationships', into its
database during synchronisation. Peer names in the branch config must match the peer names in
the hub's relationship for that branch (they are used for signalling).

## Hub config
One relationship per spoke. Peer names must be unique across all relationships (the ARM's own
example names the hub `server2` in one relationship and `server4` in the other), and every peer
on one server needs its own listener address/port pair or Kea fails to start with
"Address already in use":
```json
"high-availability": [
  { "this-server-name": "hub-b1", "mode": "hot-standby", "peers": [
      { "name": "branch1", "url": "http://10.1.0.10:8001/", "role": "primary" },
      { "name": "hub-b1",  "url": "http://10.0.0.10:8001/", "role": "standby" } ] },
  { "this-server-name": "hub-b2", "mode": "hot-standby", "peers": [
      { "name": "branch2", "url": "http://10.2.0.10:8001/", "role": "primary" },
      { "name": "hub-b2",  "url": "http://10.0.0.11:8001/", "role": "standby" } ] }
]
```
The hub's config contains all branch subnets so it can answer for a failed branch. The optional
`"server-name"` argument addresses one relationship in HA commands such as `ha-heartbeat`,
`ha-sync` and `ha-maintenance-start`.

## Requirements
- Kea 2.6.0 or later (2.5.5 development) on all servers; the ARM examples use the dedicated HTTP
  listener (`http-dedicated-listener: true` inside `multi-threading`).
- Client requests at each branch must reach both the branch server and the hub (for example a relay with both helper addresses), since the hub answers only when its relationship is `partner-down`.
- The ARM describes the arrangement with `hot-standby` relationships (branch primary, hub standby).
- Incompatible with the RADIUS hook's `reselect-subnet-address` and `reselect-subnet-pool`.

## Verify
- [ ] `status-get` on the hub lists every relationship with the partner state, and stopping a branch server moves its subnets to the hub (partner-down).
