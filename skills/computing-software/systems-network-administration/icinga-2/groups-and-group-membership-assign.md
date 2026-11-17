---
id: computing-software.systems-network-administration.icinga-2.groups-and-group-membership-assign
name: groups-and-group-membership-assign
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, hostgroup, servicegroup, usergroup, groups, assign-where]
level: practitioner
status: docs-checked
description: Create Icinga 2 HostGroup, ServiceGroup and UserGroup objects, add members via template groups += or assign where and ignore where.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/03-monitoring-basics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# groups and group membership assign
Groups are primarily a visualization aid in web interfaces.

Manual membership is set on the member object:
```
object HostGroup "windows" {
  display_name = "Windows Servers"
}
template Host "windows-server" {
  groups += [ "windows" ]
}
object Host "mssql-srv1" {
  import "windows-server"
  vars.mssql_port = 1433
}
```
Service and user groups work the same way (`UserGroup`, a `User` template with `groups += [...]`).

Automatic membership uses assign rules on the group object:
```
object HostGroup "prod-mssql" {
  display_name = "Production MSSQL Servers"
  assign where host.vars.mssql_port && host.vars.prod_mysql_db
  ignore where host.vars.test_server == true
  ignore where match("*internal", host.name)
}
```
Hosts matching `assign where` become members unless an `ignore where` also matches. Assign syntax is documented in the Language Reference under Apply.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the Groups and Group Membership Assign sections of the Icinga 2 Monitoring Basics chapter (03-monitoring-basics.md from the Icinga/icinga2 repository, the source of the cited page). Confirmed the HostGroup, template and UserGroup examples and the assign where and ignore where example. Removed the claim that groups are a handle for apply rules, which the page does not state, and corrected the Language Reference pointer to the Apply section. No commands were run.
