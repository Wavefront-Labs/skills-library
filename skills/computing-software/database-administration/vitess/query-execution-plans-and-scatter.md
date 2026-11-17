---
id: computing-software.database-administration.vitess.query-execution-plans-and-scatter
name: query-execution-plans-and-scatter
category: computing-software
field: database-administration
product: vitess
tags: [execution-plans, scatter-query, routing, queryz, vexplain, query-planning]
level: practitioner
status: docs-checked
description: "How Vitess builds execution plans from operators, what makes a query scatter to all shards, and where to observe plans with queryz and VExplain."
sources:
  - https://vitess.io/docs/25.0/concepts/execution-plans/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitess parses queries at both VTGate and VTTablet to produce a query execution plan, which depends on the query and the VSchema. The planner pushes as much work as possible down to MySQL; when it cannot, it collects input from several sources and merges the results.

A plan is a tree of operators. Each takes zero or more rows and emits zero or more rows; operators that join two branches combine two incoming streams. Evaluation starts at leaf nodes, which pull data from VTTablet, the topology service or sometimes evaluate expressions locally, and flows up to the root that returns results.

A routing operator tells Vitess where to send a piece of work: which keyspace, whether it is sharded, and for sharded keyspaces which vindex to use. A routing operator on a sharded keyspace with no vindex "scatters" to every shard. The page notes that not every query sent to several shards counts as a scatter query, so a scatter specifically means unroutable by a vindex.

To observe plans:
- cached plans at the VTGate `/queryz` endpoint;
- since Vitess 16, individual statement plans with `VExplain`.

## Checked

2026-11-08. Read in full: Execution Plans page (vitess.io docs 25.0, via the website repo markdown). Confirmed: planning at VTGate and VTTablet, operator tree and evaluation order, routing operators, scatter definition and caveat, /queryz and VExplain since Vitess 16. Removed: 'merges at VTGate' (page does not say where) and the practical-use paragraph about shard-count cost, which the page does not state.

Method: documentation only; no commands were run.
