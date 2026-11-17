---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-roles-and-rbac
name: portainer-roles-and-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [rbac, roles, privileges, teams, business-edition]
level: practitioner
status: docs-checked
description: "Understand the built-in Portainer Business Edition roles and how users or teams are paired with roles per environment or group."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/user/roles.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/user/teams/add.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Role-based access control is a Business Edition feature. A role is a predefined set of privileges, and users get privileges by being assigned roles. To grant access, pair a user or team with a role, then associate that pairing with an environment or environment group. One user or team can hold different roles in different environments.

Built-in roles:

- Environment administrator: full access in an environment, but no host management, no Portainer internal settings and no ownership changes.
- Edge administrator: full control of all Edge environments and Edge Compute features.
- Operator: visibility across the environment. On Kubernetes it can redeploy or roll back applications and edit configuration but not create or delete applications, volumes or namespaces. On Docker it cannot create, edit, delete, start or stop resources, but can view logs, attach to consoles, change resource ownership and manage registry repositories.
- Helpdesk: read-only, no container console, no volume changes.
- Namespace Operator: Operator, scoped to assigned namespaces; Kubernetes environments only.
- Standard User: complete control over resources the user (or the user's team) deploys.
- Read-Only User: read-only access to the resources they are entitled to see (resources created by members of their team, and public resources).

Teams are created under User-related, Teams: a name plus optional team leaders, who can add and remove members and promote co-leaders. Leaders are disabled when teams sync from an external provider.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Added the Docker Operator abilities, the Read-Only User role and the Kubernetes-only Namespace Operator limit.

Method: documentation only; no commands were run.
