---
id: computing-software.systems-network-administration.zabbix.user-types-permissions-and-roles
name: user-types-permissions-and-roles
category: computing-software
field: systems-network-administration
product: zabbix
tags: [users, user-roles, permissions, user-groups, super-admin, user, permission, role]
level: practitioner
status: docs-checked
description: "Grant access through user types, roles and host-group permissions, remembering that users never get host access directly."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/users_and_usergroups/permissions
  - https://www.zabbix.com/documentation/current/en/manual/web_interface/frontend_sections/users/user_roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Permissions depend on the user type, an optional user role and host access via user groups.

User types:
- User: limited menu access and no resources by default.
- Admin: wider menu access, still no host groups by default.
- Super admin: all menu sections and read-write access to all host and template groups; permissions cannot be revoked by denying specific groups.

User roles refine a type: you can only revoke permissions available to the type, never add them. Roles also control services, modules, API methods and frontend actions. Greyed-out items stay unreachable even by direct URL. Each user has exactly one role. Four defaults exist: Guest, User, Admin, Super admin; the default Super admin role cannot be changed or deleted since at least one unlimited Super admin must exist. Roles are created in Users > User roles by Super admins. Default access to new UI elements decides how new menu sections appear after an upgrade.

Caution from the docs: restricting a UI element only prevents opening that page; it does not remove access to the same data elsewhere in the interface.

Host access is granted only at group level. A user cannot be given a host or host group directly; add the user to a user group and give that group permission on the host group that contains the host. Templates work the same way through template groups. Because all access is group-based, plan host group layout around who needs to see what.

## Checked

2026-11-09. Confirmed against the Permissions page (user types, role adjustments, host access by group) and the User roles page (default roles, one role per user, grayed-out permissions, Super admin role protection, Default access to new UI elements, restrict-UI caution). Removed: the subgroups and tag filters suggestion, which the pages do not cover. User roles page read for roles overview and API/modules options only in part.
Method: documentation only; no commands were run.
