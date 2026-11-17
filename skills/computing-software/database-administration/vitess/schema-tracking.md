---
id: computing-software.database-administration.vitess.schema-tracking
name: schema-tracking
category: computing-software
field: database-administration
product: vitess
tags: [schema-tracking, vtgate, vttablet, query-planning, schema-change-signal]
level: practitioner
status: docs-checked
description: "Understand VTGate schema tracking: which queries it enables, the VTGate and VTTablet flags (schema-change-signal, schema-reload-time) and how VSchema columns override it."
sources:
  - https://vitess.io/docs/25.0/reference/features/schema-tracking/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VTGate knows table columns in two ways: an authoritative column list you supply in the VSchema, or schema tracking. When no column list is given, VTGate keeps its own authoritative list of columns for all tables from tracking.

What tracking lets VTGate plan:
1. Cross-shard `SELECT *` queries that need evaluation at VTGate.
2. Queries whose column dependencies cannot otherwise be resolved, for example unqualified columns in the projection or filter list.
3. Better evaluation of aggregations, GROUP BY, HAVING and LIMIT done at VTGate; it does not need `weight_string()` values and can compare values directly.

If tracking is disabled and no column list is in the VSchema, a set of queries is unsupported because VTGate lacks column information.

Flags:
- VTGate: `--schema-change-signal` (default `true`). VTGate listens for schema changes from VTTablet; a change triggers a `GetSchema` RPC to the tablet.
- VTTablet: `--queryserver-config-schema-change-signal` (default `true`). The tablet reports schema changes to VTGate when a DDL executes, and also checks periodically at the interval set by `--queryserver-config-schema-reload-time` (default 30 minutes).


## Checked

2026-11-04. Both mechanisms, the three planning benefits, flag names and defaults confirmed on the Schema Tracking page.

Method: documentation only; no commands were run.
