---
id: computing-software.cybersecurity-defensive.zitadel.administrator-roles-and-scopes
name: administrator-roles-and-scopes
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, administrators, iam-owner, org-owner, roles, permissions]
level: practitioner
status: docs-checked
description: "Pick the right ZITADEL administrator role at instance, organization or project level and add administrators on the resource they should manage."
sources:
  - https://zitadel.com/docs/guides/manage/console/administrators
  - https://zitadel.com/docs/concepts/structure/administrators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Administrators are users or service accounts holding a role that lets them manage ZITADEL itself. Older terms were members, memberships and managers. Add them on the resource they should manage: instance, organization, project or granted project. In the console, find ADMINISTRATORS in the details part of that resource and add a user.

Instance roles include:

- IAM_OWNER: manage the instance and all organizations with their content
- IAM_OWNER_VIEWER: view only
- IAM_ORG_MANAGER: manage all organizations including policies, projects and users
- IAM_USER_MANAGER: manage all users and their authorizations across organizations
- IAM_ADMIN_IMPERSONATOR and IAM_END_USER_IMPERSONATOR: allow impersonation of admin or end users
- IAM_LOGIN_CLIENT: the role a login UI service account needs

Organization-level roles use the ORG_ prefix (for example ORG_OWNER, ORG_USER_MANAGER), and project-level roles use PROJECT_ (for example PROJECT_OWNER).

Grant the narrowest role that works. A service account that creates users does not need IAM_OWNER. For layout advice that keeps instance administrators apart from customer organizations, see the hardening skill.

## Checked
2026-11-08. Confirmed against the ZITADEL Administrators guide and concept page: administrator levels, ADMINISTRATORS panel in the resource details, instance role list and descriptions, ORG_ and PROJECT_ role prefixes. Fixed the source URL list.
Method: documentation only; no commands were run.
