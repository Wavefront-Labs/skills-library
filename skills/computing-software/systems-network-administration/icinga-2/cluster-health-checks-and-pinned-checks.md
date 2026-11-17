---
id: computing-software.systems-network-administration.icinga-2.cluster-health-checks-and-pinned-checks
name: cluster-health-checks-and-pinned-checks
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, cluster-zone, cluster-check, health-checks, dependency, command-endpoint, pin-checks]
level: advanced
status: docs-checked
description: Monitor an Icinga 2 cluster with the cluster-zone and cluster checks, suppress child notifications with a dependency, and pin checks to an endpoint with command_endpoint.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cluster health checks and pinned checks
Network failures cause late check results or mass alarms for unknown checks, so add health checks.

**cluster-zone** tests whether a target zone is connected:
```
apply Service "agent-health" {
  check_command = "cluster-zone"
  display_name = "cluster-health-" + host.name
  vars.cluster_zone = host.name
  assign where host.vars.agent_endpoint
}
```
Prevent unwanted notifications with a dependency applied to all command-endpoint services:
```
apply Dependency "agent-health-check" to Service {
  parent_service_name = "agent-health"
  states = [ OK ]
  disable_notifications = true
  assign where host.vars.agent_endpoint
  ignore where service.name == "agent-health"
}
```
The `ignore where` avoids a self reference.

For master, satellite and agents, add both masters as Host objects and a service such as `satellite-zone-health` with `check_interval = 30s`, `retry_interval = 10s` and `vars.cluster_zone = "satellite"`. Create notification apply rules for these services too. For agents behind a satellite, define the agent-health service in the satellite's `zones.d` directory with `assign where host.zone == "satellite" && host.vars.agent_endpoint`.

**cluster** check verifies all endpoints in the current zone and directly connected zones. It cannot monitor three or more levels.

**Pin checks** to an endpoint in a zone with `command_endpoint`:
```
apply Service "disk" {
  check_command = "disk"
  command_endpoint = host.name
  assign where host.zone == "master" && match("icinga2-master*", host.name)
}
```
The host object name must match the endpoint name.

## Checked

2026-11-04. Confirmed against the Icinga 2 distributed monitoring chapter: cluster-zone and cluster checks with the 3-level limitation, dependency to suppress notifications, command_endpoint pinning.

Method: documentation only; no commands were run.
