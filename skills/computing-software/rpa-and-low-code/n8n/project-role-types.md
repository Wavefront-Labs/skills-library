---
id: computing-software.rpa-and-low-code.n8n.project-role-types
name: project-role-types
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, rbac, project-admin, project-editor, project-viewer, roles]
level: intro
status: docs-checked
description: "Compare the three n8n project roles Admin, Editor and Viewer, their plan availability and what each may do inside a project."
sources:
  - https://docs.n8n.io/administer/manage-users-and-access/set-permissions-and-roles-rbac/see-available-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose the right role when adding someone to a project. A user can hold different roles in different projects; instance roles are separate.

- **Project Admin**: manage settings (rename, delete project) and members (invite, remove, change roles); view, create, update, delete any workflows, credentials and executions in the project; create end-user credentials (by default only project admins, grantable via custom roles).
- **Project Editor**: view, create, update and delete workflows, credentials and executions in the project. Available on n8n Cloud Pro and self-hosted Enterprise.
- **Project Viewer**: effectively read-only access to all workflows, credentials and executions. Viewers cannot manually execute workflows. Available on n8n Cloud Enterprise and self-hosted Enterprise.

If none fits, create custom roles. Project roles apply to the credentials the project holds; a project role does not let you use another member's personal credential in a project workflow. Variables and tags are global to the instance and are not affected by RBAC.

## Checked
Method: docs-checked 2026-11-09 against the n8n "See available roles" page (docs.n8n.io, read in full).
Removed as not on that page: the claim that only project admins can share project-owned credentials and push project changes to Git.
