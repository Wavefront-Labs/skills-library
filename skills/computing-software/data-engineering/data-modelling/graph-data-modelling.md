---
id: computing-software.data-engineering.data-modelling.graph-data-modelling
name: graph-data-modelling
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, graph-data-model, property-graph, neo4j, relationships]
level: advanced
status: draft
description: "Design property graph models (Neo4j, Neptune, graph queries in SQL): nodes vs relationships vs properties, labels, supernodes, and when a graph model beats relational."
sources:
  - https://neo4j.com/docs/getting-started/data-modeling/
  - https://neo4j.com/docs/getting-started/data-modeling/modeling-tips/
  - https://docs.aws.amazon.com/neptune/latest/userguide/intro.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Graph data modelling

**Goal:** a graph model where the important questions are short traversals (fraud rings, recommendations, dependency/lineage, network paths).

## Building blocks (property graph)
- **Nodes** with labels (`:Customer`, `:Device`, `:Account`) and properties.
- **Relationships** with a type and direction (`(:Customer)-[:USES]->(:Device)`), which can also carry properties (`since`, `weight`).
- Rule of thumb: nouns -> nodes, verbs -> relationships, adjectives -> properties.

## Design from questions
"Which customers share a device or phone with a known fraudster within 2 hops?"
```cypher
MATCH (f:Customer {flagged: true})-[:USES|HAS_PHONE*1..2]-(c:Customer)
WHERE c <> f
RETURN DISTINCT c.id;
```
If a property is used to connect things (phone number, IP), promote it to a node so it becomes traversable.

## Choices
- Relationship vs property: model as a relationship when you traverse it or it has its own properties.
- Specific relationship types (`:PURCHASED`, `:VIEWED`) beat a generic `:INTERACTED {type}`: traversals filter by type cheaply.
- Intermediate nodes for n-ary facts (an `:Employment` node connecting person, company, role, dates).
- Time: relationship properties (`valid_from`) or time-tree nodes for heavy temporal queries.

## Supernodes
Nodes with millions of relationships (a popular IP, a "country" node) slow traversals. Avoid linking to low-information hubs; split by time or type; filter by relationship type early.

## When not to use a graph DB
Aggregations over large tables, reporting, simple one-hop joins: a relational/warehouse model is better. Recursive CTEs or SQL/PGQ graph queries may cover occasional path queries.

## Loading
Unique constraints on node keys first (`CREATE CONSTRAINT FOR (c:Customer) REQUIRE c.id IS UNIQUE`), then `MERGE` nodes, then relationships in batches.

## Verify
Key questions run as bounded traversals with `PROFILE` showing index seeks on start nodes, not label scans.
