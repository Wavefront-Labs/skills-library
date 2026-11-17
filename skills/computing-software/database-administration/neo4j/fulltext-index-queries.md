---
id: computing-software.database-administration.neo4j.fulltext-index-queries
name: fulltext-index-queries
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, create-fulltext-index, db-index-fulltext, querynodes, fulltext-index, vector-index, lucene, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Lucene search"
sources:
  - https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/full-text-indexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full-text indexes

Goal: run text search.
- `CREATE FULLTEXT INDEX titles FOR (n:Movie|Show) ON EACH [n.title, n.plot]` (labels separated by `|`).
- `CALL db.index.fulltext.queryNodes('titles', 'late') YIELD node, score`; the page notes newer syntax from version 2026.09 and says to use `queryNodes()` before that or with Cypher 5.
- Indexes are powered by Apache Lucene and return a Lucene relevance score. The default analyzer is `standard-no-stop-words`; set an index-specific one with the `fulltext.analyzer` setting.
Verify: scores rank expected results.

## Checked

2026-11-02. Confirmed: creation syntax, `queryNodes`, Lucene score, default analyzer and `fulltext.analyzer` (full-text-indexes). Removed: the fuzzy `~` query example (not shown on the page).
Method: documentation only; no commands were run.
