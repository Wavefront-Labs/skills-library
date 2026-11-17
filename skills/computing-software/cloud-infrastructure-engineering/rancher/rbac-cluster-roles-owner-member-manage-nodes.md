---
id: computing-software.cloud-infrastructure-engineering.rancher.rbac-cluster-roles-owner-member-manage-nodes
name: rbac-cluster-roles-owner-member-manage-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rbac, cluster-owner, cluster-member, role-templates, manage-nodes, create-projects, membership]
level: practitioner
status: docs-checked
description: "Rancher Cluster Owner versus Member, built-in custom cluster roles, Manage Nodes on RKE versus RKE2, and the Pod Security risk."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/manage-role-based-access-control-rbac/cluster-and-project-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Roles are managed under **Users & Authentication > Role Templates** in the **Cluster** and **Project/Namespaces** tabs. Access for non-administrators is determined by **membership** in a cluster or project. Whoever creates a cluster or project is made its `Owner` and can assign others; non-administrators see nothing by default until someone grants membership.

**Cluster Owner** has full control of the cluster. **Cluster Member** can view most cluster-level resources and create projects. A built-in custom cluster role table shows which pieces each includes:

- both: Create Projects, View Cluster Catalogs, View Cluster Members, View Nodes;
- Owner only: Manage Cluster Backups, Manage Cluster Catalogs, Manage Cluster Members, Manage Nodes, Manage Storage, View All Projects.

**Manage Nodes** covers SSH Access and Delete Nodes on both RKE and RKE2, and scaling clusters up and down on RKE; on RKE2 you must instead have permission to edit the cluster to scale.

Warning on the page: when a Cluster Member creates a project they automatically become **Project Owner**, with comprehensive control including deploying workloads. Without enforced Pod Security Standards and Pod Security Admission, that is a privilege path to review.

Assigning a custom cluster role to a new member: open the cluster, **Explore**, then **Cluster > Cluster Members > Add**, and pick the role under **Cluster Permissions**. To change an existing member's role use **Users & Authentication**, the member's **Edit Config**, and choose from the **Custom** section.

## Checked

2026-11-09. Read the cited Cluster and Project Roles page in full and checked every claim against it (Owner and Member roles, built-in role table, Manage Nodes table, Pod Security warning, assignment steps). Removed the v2.6.4 menu-path version note, which the page does not state.

Method: documentation only; no commands were run.
