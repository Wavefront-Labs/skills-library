---
id: computing-software.web-development.directus.existing-database-introspection
name: existing-database-introspection
category: computing-software
field: web-development
product: directus
tags: [existing-database, introspection, system-collections, composite-keys]
level: practitioner
status: docs-checked
description: "Connect Directus to an existing database, expose its tables as collections, and finish the metadata, permissions and relations the Studio needs."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/1.collections.md
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/2.fields.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When Directus connects to an existing database it introspects tables and relationships. Collections become available to admins through the Items API.

To make them usable:
1. For Studio access, configure each collection with Directus metadata: interfaces, displays, icons.
2. For non-admin access, configure access control for the collection like any other.
3. Add any relationship not defined in the database inside Directus.

Limits stated in the docs: no support for composite keys, and no virtual tables created via SQL views.

System collections (all prefixed `directus_`) hold Directus state, for example `directus_users`, `directus_roles`, `directus_permissions`, `directus_files`, `directus_flows`, `directus_settings`, `directus_revisions`, `directus_activity`. Their default fields cannot be altered but you can add fields to them. System collections are never treated as inactive.

## Checked

2026-11-04: introspection behaviour, the three follow-up steps, the composite keys and SQL views limitation, the directus_ system collection names, the rule that system collection fields cannot be altered but can be extended, and that system collections are never inactive confirmed against the Directus Collections page. Removed a claim about fields of supported types appearing automatically and a Verify line, neither stated on the page.

Method: documentation only; no commands were run.
