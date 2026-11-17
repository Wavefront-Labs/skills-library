---
id: computing-software.data-science-and-analytics.apache-superset.built-in-roles-permissions
name: built-in-roles-permissions
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [rbac, roles, permissions, gamma, alpha]
level: intro
status: docs-checked
description: "Understand Superset RBAC: the Admin, Alpha, Gamma, sql_lab and Public roles, Public role settings, and how superset init re-syncs permissions."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/security.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: assign the right role and avoid editing built-ins.

Built-in roles:
- **Admin**: all rights, including granting or revoking rights from other users and altering other people's charts and dashboards. Admins are treated as fully trusted.
- **Alpha**: access to all data sources, can add and alter data sources, but cannot grant or revoke access for others and can only alter objects they own.
- **Gamma**: limited; consumes data only from data sources granted through another complementary role, cannot alter or add data sources, though it can create charts and dashboards. List views show only objects it can access.
- **sql_lab**: grants access to SQL Lab. Alpha and Gamma users still need access per database. `can_estimate_query_cost on SQLLab` and `can_format_sql on SQLLab` must be granted separately (Security, List Roles).
- **Public**: the most restrictive built-in role, for anonymous users viewing dashboards; no write permissions, no SQL Lab. It applies when `AUTH_ROLE_PUBLIC` is set (a Flask-AppBuilder setting).

Public role settings: `PUBLIC_ROLE_LIKE` (optional, for example `"Public"` or `"Gamma"`) controls which permissions `superset init` syncs to Public. Public only grants UI and API permissions: dataset access must also be granted (edit the Public role under Security, List Roles) or, with `ENABLE_VIEWERS`, anonymous users see published dashboards where the Public role was added as a viewer. `VIEWER_PROMISCUOUS_MODE` can bypass dataset permission checks for viewer access.

Programmatic access: `FAB_API_KEY_ENABLED` turns on API keys; users with `can_read` and `can_write` on `ApiKey` (Admins by default) manage them.

Practices:
- Do not edit built-in roles: their permissions are re-synchronised to the original values when `superset init` runs (often between versions). Use "Copy Role" in the web UI, rename the copy and customise it.
- To customise Public, either edit it directly and leave `PUBLIC_ROLE_LIKE` unset, or copy it (for example `Public_Custom`) and point both `PUBLIC_ROLE_LIKE` and `AUTH_ROLE_PUBLIC` at the copy.

## Checked

2026-11-08. Confirmed against the Security page (provided roles, sql_lab and Public sections and role synchronization notes read; API key lines checked by search; the rest of the long page not read). Removed: the generic "view or menu plus action" permission model description, "data access per schema", "review roles after each upgrade" and "combine sql_lab with Gamma" (not stated); corrected Alpha (page says data sources, not charts and dashboards).
Method: documentation only; no commands were run.
