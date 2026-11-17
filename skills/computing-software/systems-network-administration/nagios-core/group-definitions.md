---
id: computing-software.systems-network-administration.nagios-core.group-definitions
name: group-definitions
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, hostgroup, servicegroup, contactgroup, members, hostgroup-members, servicegroup-members, contactgroup-members, group-definition]
level: practitioner
status: docs-checked
description: "Define hostgroups, servicegroups and contactgroups in Nagios Core: members versus nested *_members, the host,service pair format for servicegroups, and examples."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group definitions

All three have a name, `alias`, `members` and a nested-group directive; hostgroups and servicegroups also take `notes`, `notes_url`, `action_url`.

## hostgroup
`hostgroup_name`, `alias`, `members` (host short names), `hostgroup_members` (other hostgroups), `notes`, `notes_url`, `action_url`. Hosts may also join via their own `hostgroups` directive.

```
define hostgroup {
    hostgroup_name  novell-servers
    alias           Novell Servers
    members         netware1,netware2
}
```

## servicegroup
`members` is a flat list of host and service PAIRS: `host1,service1,host2,service2`. Each host name must precede its service description. `servicegroup_members` nests groups.

```
define servicegroup {
    servicegroup_name dbservices
    alias             Database Services
    members           ms1,SQL Server,ms1,SQL Server Agent
}
```

## contactgroup
`contactgroup_name`, `alias`, `members` (contact names), `contactgroup_members`. Hosts and services reference these through `contact_groups`; duplicates across groups are notified once.

## Tip
`members *` in a hostgroup includes all defined hosts.

Self-check: `nagios -v` passes after adding the group.

## Checked

2026-11-04. Confirmed against the Host Group, Service Group and Contact Group sections of the object definitions page: directive lists, members and nested directives, the host-then-service pair format, the hostgroup, servicegroup and contactgroup examples, and the members * wildcard on the Object Tricks page. Replaced the unconfirmed web UI self-check.

Method: documentation only; no commands were run.
