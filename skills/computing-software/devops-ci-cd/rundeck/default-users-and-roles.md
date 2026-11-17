---
id: computing-software.devops-ci-cd.rundeck.default-users-and-roles
name: default-users-and-roles
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, default-users, realm-properties, ops-admin, app-admin]
level: practitioner
status: docs-checked
description: "Know the built-in admin and user logins and the Rundeck 4.0 roles admin, ops_admin and app_admin, and what to do with the default passwords."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/security/default-users.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Installation defines two temporary logins, configured through `realm.properties`:
- `admin`, password `admin`: in the admin group, gets the `admin` and `user` roles.
- `user`, password `user`: can run commands and jobs but not modify job definitions.

The docs strongly recommend creating named admin accounts via your preferred authentication method, then securing these two by editing `realm.properties` or turning off the property file login method.

Rundeck 4.0 adds built-in roles usable in ACLs. Roles are sets of ACL actions, not groups. They apply least privilege even if ACLs grant more:
- `admin` (Full Admin): everything.
- `ops_admin`: keeps Rundeck running. No access to projects, users, tours, system calendars, schedule forecast, system ACLs or Key Storage. Can see license details and Cluster Manager. Configuration Management limited to database, file storage, server URLs and cluster settings.
- `app_admin`: uses Rundeck to automate. Full access to projects, users, tours, calendars, forecast, system ACLs and Key Storage; no Cluster Manager; minimal license details. Configuration Management limited to plugin settings, mail and GUI customisation.

Ops and App admin are intentionally inverse to allow separation of duties.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Built-In Users/Roles: admin/admin and user/user logins, realm.properties, the warning to secure them, and the Rundeck 4.0 admin, ops_admin and app_admin role restrictions and Configuration Management limits. Nothing removed.

Method: documentation only; no commands were run.
