---
id: computing-software.web-development.appwrite.appwrite-permissions-roles-model
name: appwrite-permissions-roles-model
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, security, permissions, roles, labels]
level: intro
status: docs-checked
description: "Use the Permission and Role helpers to grant read, create, update and delete access on rows, files and other resources."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/security/permissions/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/labels/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: express who can do what with Appwrite permissions.

Model: permissions are granted, never implied. Resources are databases, tables, rows, buckets and files. Types via the `Permission` class: `read()`, `create()` (not valid on files or rows), `update()`, `delete()` and `write()` (alias for create, update and delete on tables and buckets; update and delete on rows and files).

Roles via `Role`: `any()`, `guests()`, `users([status])`, `user(id, [status])`, `team(id)`, `team(id, role)`, `member(membershipId)`, and `label(labelId)`. Status can be `verified` or `unverified`.

Example: `permissions: [Permission.read(Role.any()), Permission.update(Role.team('writers')), Permission.delete(Role.user('<USER_ID>'))]`.

Labels: tags you place on users (for example `subscriber`) from a Server SDK with `users.updateLabels`, for access control with `Permission.read(Role.label('subscriber'))`; removing the label removes access.

Defaults: resources created with a Server SDK or the Console without permissions are inaccessible to everyone; created with a Client SDK, the creator gets read, update and delete.

A user can only grant permissions they hold; sharing with a team they are not in returns 401. Use a Function with a Server SDK for that case.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): advanced/security/permissions, products/auth/labels. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the invented Verify step (401 on read); added that labels are set from a Server SDK with users.updateLabels (labels page).

Method: documentation only; no commands were run.
