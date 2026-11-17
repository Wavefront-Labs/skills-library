---
id: computing-software.cybersecurity-defensive.zitadel.role-assignments-and-external-users
name: role-assignments-and-external-users
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, role-assignments, authorizations, external-users, roles]
level: practitioner
status: docs-checked
description: "Assign project roles to users in the console, including users of other organizations, and see where roles can be viewed and managed."
sources:
  - https://zitadel.com/docs/guides/manage/console/roles
  - https://zitadel.com/docs/concepts/features/external-user-grant
  - https://zitadel.com/docs/guides/manage/console/projects-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A role assignment combines a user with one or more roles of a project. Older terms were user grant and authorization.

Define roles first, in the project's Roles section. For an administration app you might create `admin` (display name Administrator, group Administration) and `account` (Accountant, group Administration). Then open Role Assignments under the project and choose New, type the username, continue, pick roles and save. Clicking a group name selects all its roles.

Users from other organizations can be assigned too. The hint below the username field starts an external user role assignment. The inviting organization then manages the external user's roles in its project, without that person joining the organization.

You can view and assign roles from the organization, the project or the users page, so use whichever matches your workflow.

Your application receives roles through the project's settings and the role scopes, described in the OIDC scopes skill. Assigning a role alone does not put it in a token unless the application requests it or the project is set to assert roles.

For programmatic use, the documentation references an API to create an authorization, the API term for a role assignment.

## Checked

2026-11-08. Read in full: the roles page, the external user role assignments page and the projects page. Removed the CreateAuthorization method name, which the pages do not give; the external user page only references an API to create an authorization.

Method: documentation only; no commands were run.
