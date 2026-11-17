---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spanner-graph-schemas-and-gql-queries
name: spanner-graph-schemas-and-gql-queries
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spanner, spanner-graph, gql, graph-database, property-graph]
level: advanced
status: docs-checked
description: "Model a property graph over Spanner tables with CREATE PROPERTY GRAPH, query it with GQL MATCH patterns, and design keys and interleaving so traversals stay fast."
sources: ["https://docs.cloud.google.com/spanner/docs/graph/schema-overview", "https://docs.cloud.google.com/spanner/docs/graph/queries-overview", "https://docs.cloud.google.com/spanner/docs/graph/best-practices-designing-schema"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spanner Graph schemas and GQL queries

Spanner Graph maps ordinary tables to nodes and edges; data stays relational, so SQL and GQL query the
same rows. Needs the Enterprise or Enterprise Plus edition.

## 1. Tables, then the graph
```sql
CREATE TABLE Person (id INT64 NOT NULL, name STRING(MAX)) PRIMARY KEY (id);
CREATE TABLE Account (id INT64 NOT NULL, blocked BOOL) PRIMARY KEY (id);
CREATE TABLE PersonOwnAccount (id INT64 NOT NULL, account_id INT64 NOT NULL, create_time TIMESTAMP)
  PRIMARY KEY (id, account_id), INTERLEAVE IN PARENT Person ON DELETE CASCADE;
CREATE TABLE AccountTransfer (id INT64 NOT NULL, to_id INT64 NOT NULL, ts TIMESTAMP NOT NULL, amount FLOAT64)
  PRIMARY KEY (id, to_id, ts), INTERLEAVE IN PARENT Account ON DELETE CASCADE;

CREATE PROPERTY GRAPH FinGraph
  NODE TABLES (Person, Account)
  EDGE TABLES (
    PersonOwnAccount SOURCE KEY (id) REFERENCES Person (id)
                     DESTINATION KEY (account_id) REFERENCES Account (id) LABEL Owns,
    AccountTransfer  SOURCE KEY (id) REFERENCES Account (id)
                     DESTINATION KEY (to_id) REFERENCES Account (id) LABEL Transfers);
```
Interleaving edges in their source node keeps outgoing traversals local to one split.

## 2. Query with GQL
```sql
GRAPH FinGraph
MATCH (p:Person {id: @pid})-[:Owns]->(a:Account)-[t:Transfers]->{1,3}(dst:Account)
WHERE dst.blocked
RETURN p.name, dst.id, ARRAY_LENGTH(t) AS hops;
```
- A quantifier such as `{1,3}` applies to the edge pattern and bounds traversal depth; prefer bounded quantifiers.
- `GRAPH_TABLE(...)` takes a linear graph query and returns tabular results inside SQL, so you can join them with normal tables.
- Spanner Graph does not support returning graph elements as query results; return properties.

## 3. Performance design
- For **incoming** (reverse) traversals, create a secondary index on the edge table's destination key, interleave it into the destination node table and store the edge properties with `STORING`; see the best-practices page for the exact DDL.
- Start patterns from a selective, keyed node; secondary indexes avoid full-table scans when looking up nodes and edges by property values.

## Gotchas
- Spanner does not allow schema changes that break graph dependencies: you cannot drop a table used by a graph until you remove its definition from the graph (`CREATE OR REPLACE PROPERTY GRAPH`).
- A label defaults to the input table name and all columns are exposed as properties; use `LABEL` and `PROPERTIES (...)` clauses to control what is exposed.

## Verify
- [ ] A sample traversal returns the expected rows.

## Checked
Checked 2026-10-24 against the Spanner Graph schema overview, queries overview and schema-design best-practices pages (docs.cloud.google.com). Confirmed the edition requirement, `CREATE PROPERTY GRAPH` node and edge table syntax with `SOURCE KEY`/`DESTINATION KEY ... REFERENCES` and `LABEL`, interleaving edges into the source node, default labels and properties, `CREATE OR REPLACE PROPERTY GRAPH`, GQL quantifiers, `GRAPH_TABLE`, parameters and the drop-dependency rule. Removed the `INFORMATION_SCHEMA.PROPERTY_GRAPHS` view name, the supernode advice and the `PROFILE` remark, and replaced the guessed index DDL with the documented pattern.
Method: documentation only; no commands were run.
