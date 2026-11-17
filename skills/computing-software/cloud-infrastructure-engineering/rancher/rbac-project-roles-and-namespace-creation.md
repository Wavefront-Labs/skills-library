---
id: computing-software.cloud-infrastructure-engineering.rancher.rbac-project-roles-and-namespace-creation
name: rbac-project-roles-and-namespace-creation
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rbac, project-owner, project-member, read-only, namespace-creation, kubernetes-edit, clusterrole]
level: practitioner
status: docs-checked
description: "Rancher Project Owner, Member and Read Only, Kubernetes admin/edit inheritance, and the cluster-wide namespace creation role."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/manage-role-based-access-control-rbac/cluster-and-project-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three primary project roles exist:

- **Project Owner** has full control of the project and its resources.
- **Project Member** manages project-scoped resources such as namespaces and workloads but cannot manage other project members.
- **Read Only** can view everything in the project but cannot create, update or delete.

By default the Rancher `project-member` role inherits from the Kubernetes `edit` role and `project-owner` inherits from `admin`. Both therefore allow namespace management, including creating and deleting namespaces.

The page flags a danger here. Users given the `owner` or `member` project role automatically inherit a **namespace creation** role, but that role is a Kubernetes **ClusterRole**, so its scope extends to every project in the cluster. Users with the owner or member role on a project can therefore create namespaces in other projects they are assigned to, even where they hold only the Read Only role. Anyone designing least-privilege access for tenants should treat namespace creation as cluster-reaching, and consider the custom project roles and locked roles described in the other RBAC skills.

Custom project roles, either built-in or admin-defined, give narrower access than Owner, Member or Read Only. You add members from the project's own membership tab, and, as with clusters, an Owner can assign other users roles within the project. For project resource limits on top of roles, see the project quota skill.

## Checked

2026-11-09. Read the cited Cluster and Project Roles page in full and checked every claim against it (three project roles, admin/edit inheritance, namespace creation ClusterRole warning). Corrected the scope of the namespace creation warning: the page says other projects the user is assigned to, not any project.

Method: documentation only; no commands were run.
