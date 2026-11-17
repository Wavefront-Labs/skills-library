---
id: computing-software.web-development.strapi.admin-roles-rbac
name: admin-roles-rbac
category: computing-software
field: web-development
product: strapi
tags: [strapi, rbac, roles, administrators, super-admin, permissions]
level: intro
status: docs-checked
description: "Admin panel roles in Strapi RBAC: the three default roles, creating, duplicating and deleting roles."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/rbac.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Admin roles (RBAC)

RBAC manages administrators (the admin panel users), their accounts and roles. Path: Settings > Administration panel > Roles.

Default roles:
- Author: create and manage their own content.
- Editor: create content, manage and publish any content.
- Super Admin: access to all features and settings; given to the first administrator.

## Actions
- **Add new role** (top right) leads to the role editor where details and permissions are set.
- Duplicate button in the table creates a role from an existing one.
- Delete: only when the role is no longer attributed to any administrator. Remove it from all admins first, then click delete and confirm.

Editing a role: set a name and description, then permissions in a table with four categories: Collection types, Single types, Plugins and Settings. Per content-type the actions are create, read, update, delete and publish, all fields allowed by default; you can untick actions or individual fields, and per locale when Internationalization is installed. The Super Admin role's permissions are read-only and cannot be edited.

Settings pages have their own permissions, for example "Access the API tokens settings page", "Access the Email settings page", and the Admin tokens and Transfer tokens settings pages with create, read, update, delete and regenerate grants.

Custom conditions: each granted permission has a Settings button for extra conditions. The two defaults are "the administrator must be the creator" and "must have the same role as the creator". They only work on permissions already ticked for the role, and more can be added in code.

Administrators are managed under Settings > Administration panel > Users: invite a user (first name, last name and email, plus a role), after which a first-login URL is shown until the account is activated.

## Checked
Confirmed 2026-11-08 against the Strapi RBAC feature page (read in full): default roles, create, duplicate and delete behaviour. Added role editing, categories, Super Admin read-only, conditions and user invitation. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08

Related: end users of your front end are managed separately by Users & Permissions (`computing-software.web-development.strapi.users-permissions-jwt`).
