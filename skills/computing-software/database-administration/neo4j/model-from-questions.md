---
id: computing-software.database-administration.neo4j.model-from-questions
name: model-from-questions
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, data-model-arrows, query-driven-model, relationship-types, graph-data-modeling, labels-vs-properties, intermediate-nodes, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Derive a Neo4j graph model from the questions it must answer: write queries first, prioritise, prototype in Arrows, test with data"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://github.com/neo4j/docs-getting-started/blob/dev/modules/ROOT/pages/data-modeling/modeling-tips.adoc", "https://github.com/neo4j/docs-getting-started/blob/dev/modules/ROOT/pages/data-modeling/data-modeling-tools.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modelling from questions

Goal: derive a graph model from the queries the application must run.

- Write the questions and queries first. They determine the structure: for example, if queries filter by a date range, the date should not be only a property on a node but a separate node or relationship; for finding similar courses, a category hierarchy makes topic searches efficient.
- You need not know the Cypher syntax yet; model around the business need.
- Prioritise: no model is best for every query. Decide which queries need maximum performance and which capabilities are critical, then choose the model that best serves them. Models can be changed later.
- Sketch in Arrows (arrows.app, a no-code whiteboard for graph models); Neo4j also lists a data modeling tool that validates models and imports Arrows JSON.
- Test: load part of the data and run the real queries. If two models compete, build a proof of concept of each (and of both together) and compare on live data.
- Refactor with Cypher mass updates across labels, properties, nodes and relationships; APOC helps with batching. Data size matters: model and query choices bite as data grows.

Verify: every question maps to a short Cypher pattern that runs acceptably on loaded sample data.

## Checked
2026-11-09

Method: read the Neo4j getting-started docs pages data-modeling/modeling-tips and data-modeling-tools (raw asciidoc). Removed: the noun/verb mapping rule and the "specific relationship types beat generic RELATED_TO" rule, which these pages do not state. Not checked: the modeling tutorial and relational-to-graph pages.
