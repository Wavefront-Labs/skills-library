---
id: computing-software.systems-network-administration.icinga-2.dependencies-and-redundancy-groups
name: dependencies-and-redundancy-groups
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, dependency, parent-host-name, disable-checks, redundancy-group, reachability, unreachable]
level: advanced
status: docs-checked
description: Define Icinga 2 Dependency objects and apply rules - parent_host_name, parent_service_name, states, disable_checks, implicit host dependency, and redundancy_group.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dependencies and redundancy groups
Dependencies determine network reachability. A service can depend on a host and vice versa; all parents are inherited, not only the immediate one. `parent_host_name` and `parent_service_name` are mandatory for service dependencies; `parent_host_name` is required for host dependencies.

Key attributes:
- `states`: parent states that keep the dependency passing; the dependency fails when the parent is not in them (e.g. `states = [ OK, Critical, Unknown ]` fails on Warning).
- `disable_notifications`: notifications are suppressed by default when unreachable.
- `disable_checks`: stop checks of the child.
- `ignore_soft_states`: set `false` to trigger on the parent's soft state.

Query `last_reachable` via the REST API. Reachability needs fresh processed check results, so disabling checks of children breaks it. Nesting depth is limited to 256.

**Implicit:** every service depends on its host, implicitly setting `disable_notifications = true` and `states = [ Up ]`; checks still run. To stop them:
```
apply Dependency "disable-host-service-checks" to Service {
  disable_checks = true
  assign where true
}
```
**Network example:** `apply Dependency "internet" to Host { parent_host_name = "dsl-router" ... assign where host.name != "dsl-router" }`.

**Redundancy groups:** all dependencies are essential by default. Giving two dependencies of a child the same `redundancy_group` value makes them redundant within that group. The docs recount that before v2.12 all were cumulative, v2.12 and v2.13 all redundant, and v2.14 restored the former behaviour.

**From vars:** `parent_host_name = host.vars.vm_parent` with `assign where "generic-vm" in host.templates`.

## Checked

2026-11-04. Confirmed against the Icinga 2 monitoring basics chapter: dependency attributes, implicit host dependency, last_reachable, nesting depth 256, redundancy_group and the v2.12 to v2.14 history.

Method: documentation only; no commands were run.
