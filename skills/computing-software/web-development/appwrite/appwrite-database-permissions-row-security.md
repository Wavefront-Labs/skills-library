---
id: computing-software.web-development.appwrite.appwrite-database-permissions-row-security
name: appwrite-database-permissions-row-security
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, permissions, row-security, tablesdb]
level: practitioner
status: docs-checked
description: "Combine table-level and row-level permissions and know when Row Security must be enabled."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/permissions/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/security/permissions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide where access is defined.

Rules from the docs:
- Permissions are granted. By default no permissions are granted, so no user can access any rows.
- Two levels exist: table level and row level. A user with access at either level can access a row; access at both is not needed.
- Table level applies to every row: configure in Your table > Settings > Permissions. A user with read, create, update or delete here can access all rows.
- Row level applies to individual rows and is applied only if Row Security is enabled: Your table > Settings > Row security. Row-level permissions are configured on the individual rows.

Defaults: a resource created with a Server SDK or the Console without explicit permissions has empty permissions, so nobody can access it. Created with a Client SDK without explicit permissions, the creator gets read, update and delete.

Private-by-creator rows (from the platform permissions page):
1. Enable Row Security in the table Settings.
2. Grant only CREATE to all users at table level. Omitting READ, UPDATE and DELETE at table level stops users reading every row.
3. When creating a row, pass `permissions: [Permission.read(Role.user('<USER_ID>')), Permission.update(Role.user('<USER_ID>')), Permission.delete(Role.user('<USER_ID>'))]`.
Other users can create their own rows but cannot access rows they did not create.

Gotchas:
- `Permission.create()` does not apply to rows or files; applying it results in an error. Use table-level create.
- A user can only grant permissions on a resource that they have; sharing a row with a team they are not in returns a 401 not authorized error. Use a Function with a Server SDK for that case.
- A Server SDK with the proper API key scopes can access any resource regardless of its permissions.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Database permissions and Permissions (advanced/security/permissions): default no-access, the two levels, Console paths, Row Security, defaults per SDK, the private rows setup and example, the `Permission.create()` restriction, the 401 sharing rule, and server access. Added the platform permissions page as a source. Removed: the claim that ignoring Row Security produces 401 on row ACLs, and the two-user Verify test, which the pages do not state.
Method: documentation only; no commands were run.
