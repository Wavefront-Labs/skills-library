---
id: computing-software.systems-network-administration.zabbix.host-groups-and-subgroups
name: host-groups-and-subgroups
category: computing-software
field: systems-network-administration
product: zabbix
tags: [host-groups, subgroups, permissions, nested-groups, host, group, subgroup]
level: intro
status: docs-checked
description: "Organise hosts into groups and nested subgroups, and understand how permissions flow to them."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/hosts/host_groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Host groups logically group hosts and carry user permissions. Every host needs at least one group and may be in several. All permissions in Zabbix are based on groups: user groups, host groups and template groups. Even one user needing one host is granted by a user group with permission to a host group containing it.

Only Super admin users can create host groups: Data collection > Host groups > Create host group, or type a non-existing name in a host's Host groups field.

Deleting a host group removes only the group, not its hosts. A group that is the only group of an existing host cannot be deleted.

Subgroups use a forward slash in the name: Europe/Latvia is a child of Europe, and Europe/Latvia/Riga/Zabbix servers nests several levels. Leading, trailing or repeated slashes are not allowed, and slashes cannot be escaped. Parent groups are not created automatically when you create a subgroup.

Permission inheritance:
- Creating a subgroup under an existing parent: user group permissions are inherited from the parent.
- Creating a parent over an existing subgroup: no permissions are set on the parent.
- Apply permissions and tag filters to all subgroups, when editing a group, copies the same permissions and tag filters to all current and future subgroups. It is not saved in the database, overrides existing permissions, and can be reverted only manually.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Host groups (current): group purpose, one group minimum per host, group-based permissions, Super admin only creation and both creation routes, deletion rules, subgroup naming and slash rules, no automatic parent creation, permission inheritance cases, the apply-to-subgroups option.

Method: documentation only; no commands were run.
