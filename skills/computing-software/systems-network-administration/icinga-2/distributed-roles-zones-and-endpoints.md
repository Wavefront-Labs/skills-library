---
id: computing-software.systems-network-administration.icinga-2.distributed-roles-zones-and-endpoints
name: distributed-roles-zones-and-endpoints
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, distributed-monitoring, zone, endpoint, master, satellite, agent, apilistener]
level: practitioner
status: docs-checked
description: "Model a distributed Icinga 2 setup: master, satellite and agent roles, Zones, Endpoints, zone HA, ApiListener and FQDN naming."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# distributed roles, zones and endpoints
**Roles.** A `master` has no parent (usually runs Icinga Web 2 and combines results into backends and notifications). A `satellite` has a parent and children, may run checks or delegate them, receives configuration from its parent and keeps running when the master is temporarily unavailable. An `agent` only has a parent and either runs its own checks or receives command execution events. (Older docs said "Icinga client".)

**Zones** build the trust hierarchy:
```
object Zone "master" {}
object Zone "satellite region 1" {
  parent = "master"
}
```
Child zone members may not send configuration to the parent; the master zone can send configuration to satellites. Agents get their own zone, named by convention after the FQDN.

**Endpoints** are the nodes in a zone, with connection information:
```
object Endpoint "icinga2-satellite1.localdomain" {
  host = "192.168.56.105"
}
object Zone "satellite" {
  endpoints = [ "icinga2-satellite1.localdomain" ]
  parent = "master"
}
```
Endpoints in one zone form an HA setup; two nodes in the master zone load-balance check execution. A known issue exists with more than two endpoints in a zone (a message routing loop); config validation logs a warning. To check node availability you still need a Host object.

**ApiListener** (`/etc/icinga2/features-enabled/api.conf`, enable with `icinga2 feature enable api`) loads TLS certificates and sets `accept_commands` and `accept_config`. It shares host and port with the REST API.

**Conventions:** use FQDNs; the certificate CN, the Endpoint object and the `NodeName` constant must be identical.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/. No commands were run.
