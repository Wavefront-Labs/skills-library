---
id: computing-software.data-engineering.trino.trino-resource-groups-managers
name: trino-resource-groups-managers
category: computing-software
field: data-engineering
product: trino
tags: [resource-groups, resource-group-manager, file-manager, db-manager, selectors-table]
level: advanced
status: docs-checked
description: "Configure Trino resource groups with the file-based or database-backed manager, including refresh intervals, the three tables and selector priority."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/resource-groups.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino resource groups managers

Resource groups limit resource use and queue queries. A query belongs to one group and consumes resources from it and its ancestors. Except for the queued-query limit, a group that runs out of a resource does not fail running queries; new ones queue. A group may have sub-groups or accept queries, not both.

Enable a manager in `etc/resource-groups.properties` by setting `resource-groups.configuration-manager` to `file` or `db`.

File manager:

```text
resource-groups.configuration-manager=file
resource-groups.config-file=etc/resource-groups.json
```

The path is absolute or relative to the data directory; the JSON file only needs to exist on the coordinator.

Database manager (MySQL, PostgreSQL or Oracle):

```text
resource-groups.configuration-manager=db
resource-groups.config-db-url=jdbc:mysql://localhost:3306/resource_groups
resource-groups.config-db-user=username
resource-groups.config-db-password=password
```

Tables `resource_groups_global_properties`, `resource_groups` and `selectors` are created automatically if missing. Selector rows are processed in descending `priority`. The `environment` column in `resource_groups` is matched against `node.environment`, so several clusters can share one database. Configuration reloads every second (`resource-groups.refresh-interval`, default `1s`); `resource-groups.max-refresh-interval` (default `1h`) is how long the cluster keeps accepting queries on stale configuration after refresh failures. `resource-groups.exact-match-selector-enabled` (default `false`) adds an `exact_match_source_selectors` table for exact source, environment and query type matches.

## Checked

2026-11-04. Read against the Trino docs page `admin/resource-groups.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
