---
id: computing-software.cybersecurity-defensive.zitadel.project-grants-and-delegated-roles
name: project-grants-and-delegated-roles
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, project-grants, delegation, b2b, self-service]
level: practitioner
status: docs-checked
description: "Delegate selected roles of a project to another organization so partners can assign them to their own users without administrator access."
sources:
  - https://zitadel.com/docs/concepts/structure/granted_projects
  - https://zitadel.com/docs/concepts/features/external-user-grant
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A project grant gives another organization a chosen subset of your project's roles. The receiving organization then creates role assignments for its own users by itself.

The documentation's example is a SaaS provider with roles for Sales and Accounting. When a client purchases the service, the provider grants the `sales` and `accounting` roles to that client's organization, and the client decides which of its employees get which role.

Pick the mechanism that matches the delegation you want:

- Project grant: delegates management of a whole project, or selected roles, to another organization.
- External user role assignment: gives specific users from another organization access to your project, with the inviting organization controlling those roles.

A user account is unique across a ZITADEL instance. If a person needs access to several tenants, an external role assignment is a simple alternative to creating multiple accounts.

For consumer plus staff setups, keep customers in one organization and put your own team, projects and applications in a second organization. Grant the projects to the customer organization and give staff external role assignments there, rather than duplicating staff accounts.

## Checked

2026-11-08. Read in full: the granted projects page and the external user role assignments page. All claims confirmed.

Method: documentation only; no commands were run.
