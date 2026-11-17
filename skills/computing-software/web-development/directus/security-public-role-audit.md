---
id: computing-software.web-development.directus.security-public-role-audit
name: security-public-role-audit
category: computing-software
field: web-development
product: directus
tags: [public-role-audit, public-file-folder, unauthenticated-test, public-policies-api]
level: advanced
status: docs-checked
description: "Audit and lock down the Directus Public role: item rules, a public files folder filter, an unauthenticated endpoint test, and API queries listing public permissions."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/14.security/1.best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every policy on the Public role applies to anyone, including bots. Read access with no filter exposes all items in the collection.

Rules:
- Grant public access only to collections meant for unauthenticated use; use item rules and field permissions for subsets (e.g. published only).
- Never give a public policy read on `directus_files` without a filter: it exposes `/files` and `/assets/:id`, including library exports. Restrict to a folder:

```json
{ "folder": { "_eq": "<public-folder-id>" } }
```

  Use `_in` for several folders, and set the **Default Exports Folder** (Settings > Files & Storage) to a folder no public policy can read.
- Avoid any permission on `directus_*` collections; never create, update or delete.

Audit as admin:

```http
GET /access?filter[role][_null]=true&filter[user][_null]=true&fields=policy
GET /permissions?filter[policy][_in]=<policy-id-1>,<policy-id-2>
```

Review results with a `directus_` collection or a read action with empty `permissions`. Also check Settings > User Roles > Public for extra policies.

Test unauthenticated: the page says `GET /files` with no token should return a permissions error or only files from your public folders.

## Checked

2026-11-04: Public role exposure, filter-less directus_files read risk, folder filter with _eq and _in, Default Exports Folder, the two audit API queries and review criteria confirmed against the Directus Security Best Practices page.

Method: documentation only; no commands were run.
