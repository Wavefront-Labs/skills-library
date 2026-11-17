---
id: computing-software.systems-network-administration.virtualisation.proxmox-roles-acl-and-resource-pools
name: proxmox-roles-acl-and-resource-pools
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-roles, pve-acl, pve-resource-pool, pveum, privileges, delegation, multi-tenant, proxmox, proxmox-ve, pveum-group, pveum-permissions]
level: practitioner
status: docs-checked
description: "Delegate Proxmox VE access: built-in and custom roles, ACL paths (/vms, /storage, /pool, /sdn), propagation, and resource pools to give a team its own VMs and storage."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_permission_management
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveum_pools
  - https://github.com/proxmox/pve-docs/blob/master/pveum.adoc
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Proxmox roles, ACLs and resource pools

**Goal:** teams manage their own guests without seeing or touching anyone else's, with
least privilege.

## Model
Permission = (user/group/token) + role + **path** + propagate flag (set by default).
Example paths: `/` (everything), `/vms`, `/vms/{vmid}`, `/storage/{storeid}`, `/nodes/{node}`, `/pool/{poolname}`, `/access/groups`, `/access/realms/{realmid}`.
Built-in roles: `Administrator`, `PVEAdmin` (most tasks, but no rights to modify system settings), `PVEVMAdmin` (fully administer VMs), `PVEVMUser` (view, backup, configure CD-ROM, console, power management), `PVEDatastoreUser` (allocate backup space and view storage), `PVEAuditor` (read only), `PVEPoolAdmin` (allocate pools), `PVEPoolUser` (view pools), `PVESDNUser` (access to bridges and vnets), `NoAccess` (no privileges, used to forbid access).

## Resource pools for delegation
A pool is a set of VMs, containers and storage; setting permissions on `/pool/{poolid}` applies them to all members, which is the simplest way to delegate.
```sh
pveum group add team-a-ops --comment "Team A operations"
pveum pool add team-a --comment "Team A guests"
pveum acl modify /pool/team-a --groups team-a-ops --roles PVEVMAdmin
pveum acl modify /storage/team-a-lvm --groups team-a-ops --roles PVEDatastoreUser
```
Add guests and storage to the pool in the GUI (Datacenter -> Pool -> Members) or through the pools API (`vms` and `storage` lists); the older per-pool update endpoint is marked deprecated in the source in favour of one that also supports nested pools, so check the API viewer for your release. The guide's own example grants `PVEAdmin` on `/pool/dev-pool/` to a group of developers.

## Custom role
```sh
pveum role add VMOperator --privs "VM.PowerMgmt VM.Console VM.Audit VM.Backup"
```
The guide's example is `pveum role add VM_Power-only --privs "VM.PowerMgmt VM.Console"`; the admin guide lists all privileges. Handle `Permissions.Modify` and `Sys.Modify` with care.

## Rules
- Permissions propagate down the path tree by default; permissions on deeper levels replace those inherited from above.
- Permissions for individual users always replace group permissions; group permissions apply to its members.
- `NoAccess` cancels all other roles on a path.
- A privilege-separated token can never have permissions on a path that its user does not have.

## Audit
`pveum acl list` and `pveum user permissions <user>@<realm> --path /` show effective rights.

## Verify
Log in as a team member: only pool guests and allowed storage/vnets are visible; creating a
VM outside the pool is denied; `pveum user permissions` matches the design.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17).

Confirmed: role descriptions, templated path examples, inheritance rules (propagate default, deeper paths replace inherited, user replaces group, NoAccess cancels, token limits), pool semantics and the `PVEAdmin` on `/pool/dev-pool/` example, `pveum pool add`, `pveum group add`, `pveum role add --privs`, `pveum acl modify ... --groups/--roles`. Removed as unconfirmed: the `/sdn/zones/...` and `/mapping/pci/...` example paths and the PVESDNUser ACL command on a zone path, the `Pool.Allocate` requirement for creating guests in a pool, and the `pveum pool modify` command (members are added in the GUI or API).

Method: documentation only; no commands were run.
