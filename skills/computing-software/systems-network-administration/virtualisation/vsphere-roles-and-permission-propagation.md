---
id: computing-software.systems-network-administration.virtualisation.vsphere-roles-and-permission-propagation
name: vsphere-roles-and-permission-propagation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-rbac, vsphere-security, vsphere-roles, permission-propagation, global-permissions, least-privilege, no-access-role, vmware, vcenter, vsphere]
level: practitioner
status: draft
description: "Design vCenter RBAC: custom roles from privileges, where to assign permissions, propagation and override rules, global permissions, No Access, and auditing who has what."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security-8-0/vsphere-permissions-and-user-management-tasks.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSphere roles and permission propagation

**Goal:** people and service accounts get exactly the rights they need on exactly the
objects they manage, and you can explain any user's effective rights.

## Building blocks
- **Privilege:** a single action (e.g. `VirtualMachine.Interact.PowerOn`).
- **Role:** a named set of privileges. Built-ins: Administrator, Read-only, No access,
  No cryptography administrator, plus sample roles. **Clone** samples; don't edit
  built-ins.
- **Permission:** principal (user or group) + role + object + "propagate to children".
- **Global permissions:** assigned at the SSO level, apply across all linked vCenters and
  to non-inventory objects (tags, content libraries). Needed for tag and library rights.

## Resolution rules
1. Permissions on a child object **override** those inherited from parents.
2. A permission on the **user** overrides one on a group the user is in, at the same object.
3. Multiple groups at the same object: the union of privileges.
4. **No access** explicitly assigned blocks everything at that object and below (unless
   overridden deeper).

## Design pattern
- Assign at **folders** (VM folders, host and cluster folders, datastore folders,
  network folders), not at individual VMs.
- Service accounts get minimal custom roles: backup (VADP privilege list from the
  vendor), monitoring (Read-only + specific), automation (scoped to a folder).
- Keep a "vSphere-Admins" AD group as the only Administrator at the root.
- Remember the inventory has four hierarchies: a VM permission does not grant rights on
  its datastore or network; operators deploying VMs need `Datastore.AllocateSpace` and
  `Network.Assign` on those objects too.

## Audit
```powershell
Get-VIPermission | Select Entity, Principal, Role, Propagate | Sort Principal
Get-VIRole | Where {-not $_.IsSystem} | Select Name, @{n='Privs';e={$_.PrivilegeList.Count}}
```
Check for individual users with permissions, Administrator on low objects, and stale
principals from deleted accounts.

## Verify
Log in as a member of each role group and confirm allowed and blocked actions; the
permission report contains only groups and documented service accounts.
