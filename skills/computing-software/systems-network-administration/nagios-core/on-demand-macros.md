---
id: computing-software.systems-network-administration.nagios-core.on-demand-macros
name: on-demand-macros
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, on-demand-macros, group-macros, hostmacro, servicemacro, delimiter, check-cluster-macros]
level: advanced
status: docs-checked
description: "Read another host or service's state from a Nagios Core command with on-demand macros, and aggregate across a group with a delimiter."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/macros.html
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/clusters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-demand macros

Get a value for an object other than the one being checked.

- Host: `$HOSTMACRO:host_name$`, e.g. `$HOSTSTATEID:host1$`
- Service: `$SERVICEMACRO:host_name:service_description$`, e.g. `$SERVICESTATEID:host1:DNS Service$`. An empty host name uses the service's own host.
- Contacts, contactgroups, hostgroups, servicegroups too: `$CONTACTEMAIL:john$`.

## Group form
`$HOSTMACRO:hostgroup_name:delimiter$`, `$SERVICEMACRO:servicegroup_name:delimiter$`, `$CONTACTMACRO:contactgroup_name:delimiter$`. The delimiter separates each member's value: `$HOSTSTATEID:hg1:,$` returns comma-separated state IDs.

## Limits
- On-demand macros are not exported as environment variables.
- `$ISVALIDTIME:$` and `$NEXTVALIDTIME:$` are on-demand only and take a timeperiod.

## Use
Feeds `check_cluster` (see `computing-software.systems-network-administration.nagios-core.check-cluster-monitoring`).

## Checked

2026-11-04. Confirmed against the Macros page (host, service and group on-demand formats, empty host name, contact examples, $HOSTSTATEID:hg1:,$ delimiter example, not exported to the environment), the Macro list page ($ISVALIDTIME and $NEXTVALIDTIME on-demand macros with a timeperiod) and the Clusters page ($SERVICESTATEID:host1:DNS Service$).

Method: documentation only; no commands were run.
