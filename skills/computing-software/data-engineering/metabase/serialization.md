---
id: computing-software.data-engineering.metabase.serialization
name: serialization
category: computing-software
field: data-engineering
product: metabase
tags: [serialization, export-import, entity-id, tgz, content-migration]
level: advanced
status: docs-checked
description: "Move Metabase content between instances with serialization export and import: CLI flags, API endpoints, what is included or excluded, entity_id matching and gotchas."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/serialization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Availability: Pro or Enterprise, self-hosted or Cloud.

CLI: `java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar export <dir_name> [flags]` and `... import <path>`.

Export flags: `-c, --collection <ID,...>` (personal collections otherwise excluded), `-C, --no-collections`, `-S, --no-settings`, `-D, --no-data-model`, `-f, --include-field-values` (off by default).

API: `POST /api/ee/serialization/export` streams a `.tgz`; `POST /api/ee/serialization/import` takes multipart `file=@x.tgz` and is synchronous, so large imports can time out (check server logs). Use `-H 'X-API-Key: KEY'`. Create archives with `tar -czf`.

Included: collections, dashboards, questions, models, metrics, segments, snippets, transforms, actions, data model metadata. Excluded: users, groups, permissions, alerts, subscriptions, database connection strings and license tokens (add the token manually, e.g. `MB_PREMIUM_EMBEDDING_TOKEN`).

Import behaviour: items match by `entity_id`; matches are overwritten, nothing is deleted on the target. Referenced databases, tables and fields must already exist there. Databases are referenced by name.

Gotchas:
- The docs state serialization is not meant to back up Metabase.
- Source and target should run the same major version; a mismatch only logs a warning.
- With H2 as the application database, stop Metabase before export or import.
- Trailing whitespace in native queries collapses the YAML into one string.
- Duplicating content within one instance is unsupported.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Serialization: Pro/Enterprise availability, export flags and API parameters, endpoints and synchronous import, tgz and tar commands, included and excluded entities, entity_id matching and overwrite behaviour, database references by name, same-major-version rule, H2 caveat, license token exclusion, trailing-whitespace YAML note, no-backup guidance. Nothing removed.
Method: documentation only; no commands were run.
