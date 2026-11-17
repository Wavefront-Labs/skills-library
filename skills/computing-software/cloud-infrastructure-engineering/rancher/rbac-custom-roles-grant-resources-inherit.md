---
id: computing-software.cloud-infrastructure-engineering.rancher.rbac-custom-roles-grant-resources-inherit
name: rbac-custom-roles-grant-resources-inherit
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rbac, custom-roles, role-templates, inherit-from, grant-resources, manage-roles, privilege-escalation]
level: advanced
status: docs-checked
description: "Build custom Rancher global, cluster or project roles: grant resources and verbs, inherit roles, creator defaults, deletion effects."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/manage-role-based-access-control-rbac/custom-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Roles decide what a user can do inside a cluster or project; permissions decide which clusters and projects they can reach. The page warns that a custom role can enable **privilege escalation**. You need the Administrator global permission, or custom global permissions including **Manage Roles**, to create them.

Go to **Users & Authentication > Role Templates**, choose a tab by scope (**Global**, **Cluster**, **Project/Namespaces**), click **Create Global Role**, **Create Cluster Role** or **Create Project/Namespaces Role**, and name it.

- **Cluster/Project Creator Default** assigns the role automatically to whoever creates a cluster or project. Out of the box those defaults are Cluster Owner and Project Owner.
- **Grant Resources** assigns Kubernetes API endpoints and the allowed verbs (Create, Delete, Get and so on). Use the Resource field to search predefined resources or type a custom name, then select it from the dropdown. A line marked `(Custom)` just means several API resources are grouped.
- **Inherit from** copies other Rancher roles into yours. Only cluster and project/namespace roles can inherit. A parent role cannot be deleted until its child is.

Inheritance suits groups needing near-identical access: clone an existing role such as Administrator and configure only the differences.

Deleting a custom role also deletes all global role bindings that use it. A user whose only role was deleted loses Rancher access until an administrator applies new global permissions. Built-in roles cannot be deleted.

Custom roles can be assigned to a group so the role takes effect on the members' first sign-in.

## Checked

2026-11-09. Read the cited Custom Roles page in full and checked every claim against it (prerequisites, role scopes, creator defaults, Grant Resources, Inherit from, deletion, group assignment). Removed the "danger box" wording, which the page does not state.

Method: documentation only; no commands were run.
