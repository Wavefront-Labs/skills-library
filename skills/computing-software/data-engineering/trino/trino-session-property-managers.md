---
id: computing-software.data-engineering.trino.trino-session-property-managers
name: trino-session-property-managers
category: computing-software
field: data-engineering
product: trino
tags: [session-property-manager, session-property-config, match-rules, client-tags, resource-group]
level: advanced
status: docs-checked
description: "Apply default session properties to subsets of Trino workloads with the file-based session property manager and its JSON match rules."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/session-property-managers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino session property managers

Administrators can set default session properties for parts of the workload; users can override them if authorised. Properties can control resource use, toggle features and change query characteristics. Managers are pluggable.

Enable the built-in file manager with `etc/session-property-config.properties`:

```text
session-property-config.configuration-manager=file
session-property-manager.config-file=etc/session-property-config.json
```

The path may be absolute or relative to the Trino data directory. The JSON file is a list of match rules. Every matching rule contributes properties; rules apply in file order and later rules override earlier values.

Match fields (all optional except `sessionProperties`):
- `user`: regex on the username.
- `source`: regex on the source string.
- `queryType`: one of `DATA_DEFINITION`, `DELETE`, `DESCRIBE` (also SHOW), `EXPLAIN`, `INSERT` (also CREATE TABLE AS), `SELECT`.
- `clientTags`: every listed tag must be in the query's client tags.
- `group`: regex on the fully qualified resource group name.
- `sessionProperties`: string map of system or catalog property names to string values, whatever the real type.

Example from the docs: `global.*` gets `query_max_execution_time` of `8h`; `global.interactive.*` gets `1h`; `global.pipeline.*` with client tag `etl` gets `scale_writers=true` and `hive.insert_existing_partitions_behavior=overwrite`.

## Checked

2026-11-04. Read against the Trino docs page `admin/session-property-managers.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
