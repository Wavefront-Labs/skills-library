---
id: computing-software.web-development.appwrite.appwrite-multi-tenancy-with-teams
name: appwrite-multi-tenancy-with-teams
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, auth, teams, multi-tenancy, saas, permissions]
level: practitioner
status: docs-checked
description: "Model SaaS tenants as Appwrite teams so rows and files are isolated by team-based permissions without changing code per tenant."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/auth/multi-tenancy/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/security/permissions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: one backend serving many organizations with data isolation.

Pattern from the docs: create one team per tenant, add members as team memberships with roles, secure resources with team permissions, and query normally.

Steps:
1. When a tenant signs up, create a dedicated team (`teams.create`). That team is the tenant's isolated environment.
2. Invite users via memberships and give each a role (for example admin or member); roles are matched in permissions.
3. When creating a row or file, set permissions such as `Permission.read(Role.team('<TEAM_ID>'))` and `Permission.write(Role.team('<TEAM_ID>', ['admin']))`.
4. Query with the user's own session: they automatically see only rows whose permissions match their team memberships.

Typical uses listed: SaaS organizations, collaborative tools with access levels, schools with teachers and students, department-based business software. The docs say this scales to unlimited tenants without code changes.

Gotcha: enable Row Security in the table's Settings for per-row permissions to apply.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/auth/multi-tenancy, advanced/security/permissions. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Permission.update changed to Permission.write (the page uses write); removed the unverified Verify step; Gotcha cut to the Row Security setting only (the file/bucket half is not on the pages).

Method: documentation only; no commands were run.
