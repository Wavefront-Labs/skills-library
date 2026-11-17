---
id: computing-software.systems-network-administration.proxmox-ve.access-roles-acls-and-pools
name: access-roles-acls-and-pools
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [pveum, acl, roles, resource-pool]
level: practitioner
status: docs-checked
description: "Grant Proxmox VE permissions with pveum roles, ACL paths, groups and resource pools, including auditors and delegated user admins."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pveum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Permissions are (path, user, role) or (path, group, role) or (path, token, role) entries in the ACL tree. Roles bundle privileges, and assigned roles propagate down the tree when the propagate flag is set. Useful built-in roles: `PVEAdmin` (most tasks, but not system settings), `PVEVMAdmin` (fully administer VMs), and `PVEAuditor` (read only).

Examples:

```
pveum user add testuser@pve -comment "Just a test"
pveum passwd testuser@pve
pveum group add admin -comment "System Administrators"
pveum user modify testuser@pve -group admin
pveum acl modify / -user joe@pve -role PVEAuditor
pveum acl modify /vms -user joe@pve -role PVEAuditor
```

The first ACL gives read only access to everything, the second only to virtual machines.

Delegate user management with the `PVEUserAdmin` role on `/access`. This is powerful, so limit it by realm and group:

```
pveum acl modify /access/realm/pve -user joe@pve -role PVEUserAdmin
pveum acl modify /access/groups/customers -user joe@pve -role PVEUserAdmin
```

Joe can then add users only in realm `pve` who belong to group `customers`.

Resource pools delegate a set of guests and storages to a team:

```
pveum group add developers -comment "Our software developers"
pveum user add developer1@pve -group developers -password
pveum pool add dev-pool --comment "IT development pool"
pveum acl modify /pool/dev-pool/ -group developers -role PVEAdmin
```

## Checked

2026-11-09. Compared with the Roles, Permission Management, Pools and delegation examples of https://pve.proxmox.com/pve-docs/chapter-pveum.html; role descriptions and every pveum example match.

Method: documentation only; no commands were run.

