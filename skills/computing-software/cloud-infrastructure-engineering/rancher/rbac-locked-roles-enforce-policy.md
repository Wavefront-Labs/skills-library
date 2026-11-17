---
id: computing-software.cloud-infrastructure-engineering.rancher.rbac-locked-roles-enforce-policy
name: rbac-locked-roles-enforce-policy
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rbac, locked-roles, role-templates, cluster-member, create-projects, policy-enforcement]
level: advanced
status: docs-checked
description: "Lock Rancher cluster or project roles so they cannot be newly assigned, what locking leaves unchanged, and a policy removing project creation."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/manage-role-based-access-control-rbac/locked-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A role set to `locked` cannot be assigned to users who do not already hold it, and it disappears from the **Member Roles** dropdown when adding users to a cluster or project. Users who already have the role keep the access it gives them; locking is not revocation.

Only cluster roles and project/namespace roles can be locked. Global roles cannot. The people who can lock a role are users with the `Administrator` global permission, and users with the `Custom Users` permission plus the `Manage Roles` role.

Lock or unlock under **Users & Authentication > Role Templates**, on the **Cluster** or **Project/Namespaces** tab, via the role's **Edit Config**. You can also set the lock while adding a custom role.

The page's example is a policy that cluster users must not create projects. Before adding users, lock `Cluster Owner`, `Cluster Member` and `Create Projects`. Then create a custom role with the same permissions as Cluster Member minus the ability to create projects, and use that when adding users to the cluster.

Locking does not affect users assigned the role before the lock, so (as the page does) lock the roles before adding new users to the cluster.

## Checked

2026-11-09. Read in full the Rancher Manager Locked Roles page (manage-role-based-access-control-rbac/locked-roles). Replaced an inference about existing Cluster Members with what the page states.

Method: documentation only; no commands were run.
