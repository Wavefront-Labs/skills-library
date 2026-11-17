---
id: computing-software.database-administration.vitess.routing-rules-and-view-routing
name: routing-rules-and-view-routing
category: computing-software
field: database-administration
product: vitess
tags: [routing-rules, vtctldclient, traffic-switching, applyroutingrules, views, enable-views]
level: advanced
status: docs-checked
description: "View and write Vitess routing rules with GetRoutingRules and ApplyRoutingRules: from_table and to_tables, tablet types, escaping, view routing flags."
sources:
  - https://vitess.io/docs/25.0/reference/features/schema-routing-rules/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Routing rules are global JSON that tell VTGate where queries for a table go. MoveTables and Reshard create and manage them automatically through VReplication, so reading them is the way to debug a migration. View them with `vtctldclient GetRoutingRules`; change them with `vtctldclient ApplyRoutingRules`.

Format: `{"rules": [{"from_table": "customer.customer", "to_tables": ["commerce.customer"]}]}`. Rules to remember:
- `to_tables` must contain exactly one fully qualified table.
- A keyspace-qualified `from_table` redirects any query referencing it, including unqualified references made while connected to that keyspace.
- Append `@<type>` (for example `commerce.corder@replica`) to redirect only queries for that tablet type. There is no SQL syntax for a tablet type in a table reference; select it with `use customer@replica` or the connection string.
- More specific rules win, so `customer.customer@replica` beats `customer.customer` for replica traffic.
- Escape special characters in `to_tables` with MySQL backticks, but do not escape `from_table`: redirect table `b.c` to `c.b` in keyspace `a` with from `a.b.c` and to `a.`c.b``.

Before switching traffic, MoveTables rules send every keyspace reference (plain, `@replica`, `@rdonly`) to the source keyspace.

Views (documented since v24): the same ApplyRoutingRules works for views; VTGate rewrites a query on the source view using the target view's definition. This requires `--enable-views` on VTGate and `--queryserver-enable-views` on VTTablet so the schema tracker follows views.

## Checked

2026-11-08. Read in full: Schema Routing Rules page (vitess.io docs 25.0, via the website repo markdown). Confirmed: GetRoutingRules and ApplyRoutingRules, JSON format, the single fully qualified to_tables rule, keyspace and tablet-type qualification, specificity, backtick escaping, the pre-switch MoveTables example and the view routing flags (since v24.0). Nothing removed.

Method: documentation only; no commands were run.
