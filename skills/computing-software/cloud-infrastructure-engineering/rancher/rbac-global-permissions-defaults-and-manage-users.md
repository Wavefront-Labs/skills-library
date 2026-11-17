---
id: computing-software.cloud-infrastructure-engineering.rancher.rbac-global-permissions-defaults-and-manage-users
name: rbac-global-permissions-defaults-and-manage-users
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rbac, global-permissions, administrator, standard-user, user-base, new-user-default, manage-users]
level: practitioner
status: docs-checked
description: "Rancher global roles: Administrator, Standard User, User-Base, New User Default, modular permissions, and the Manage Users risk."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/manage-role-based-access-control-rbac/global-permissions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global permissions govern authorization outside any particular cluster. The built-in ones cannot be edited or deleted: **Administrator** (full control of Rancher and all clusters), **Standard User** (can create clusters and use them, and grant others access to them) and **User-Base** (login only).

Assignment differs by user type. For a local user you pick the permission in the **Add User** form. A user logging in for the first time through an external provider automatically gets the **New User Default** permissions, which is Standard User unless changed. You can see and change the defaults under **Users & Authentication > Role Templates**, **Global** tab, **New User Default** column. Permissions can also be set per user, or for a whole group when the provider supports groups.

For narrower access, the built-in permissions are modular. Administrator includes them all; Standard User includes Create Clusters, Use Catalog Templates and User-Base (the page's prose; its table also ticks Create RKE Templates, so check the Role Templates page on your version). The ones reserved to Administrator are Manage Authentication, Manage Catalogs, Manage Cluster Drivers, Manage Node Drivers, Manage PodSecurityPolicy Templates, Manage Roles, Manage Settings and Manage Users. Combine them to build a restrictive profile instead of using Standard User.

The page warns on **Manage Users**: it lets the holder create, modify and delete other users, so giving it to non-trusted or lower-privileged users is a serious security risk and may result in privilege escalation.

The UI does not show every rule inside a permission; the full rules are visible through the API at `/v3/globalRoles`. Custom GlobalRoles can be made in the UI or via the Kubernetes API, and Rancher respects the `escalate` and `bind` verbs much as Kubernetes does.

## Checked

2026-11-09. Read the cited Global Permissions page in full and checked every claim against it (built-in permissions, assignment for local and external users, modular permission table, Manage Users warning, /v3/globalRoles, escalate and bind). Rewrote the Standard User composition to follow the page prose, which conflicts with its table.

Method: documentation only; no commands were run.
