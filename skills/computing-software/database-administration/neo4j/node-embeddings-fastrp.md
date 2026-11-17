---
id: computing-software.database-administration.neo4j.node-embeddings-fastrp
name: node-embeddings-fastrp
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, fastrp, node2vec, embedding-dimension, node-embeddings, link-prediction, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Embeddings pipeline"
sources: ["https://neo4j.com/docs/graph-data-science/current/machine-learning/node-embeddings/fastrp/", "https://neo4j.com/docs/graph-data-science/current/common-usage/running-algos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node embeddings

Goal: produce embeddings.
- FastRP is run through `gds.fastRP.stream` (and the other execution modes); `embeddingDimension` is required and sets the output array size.
- `iterationWeights` weights the intermediate embedding of each iteration; `featureProperties` with a positive `propertyRatio` mixes in node property values.
- Execution modes are `stream`, `stats`, `mutate` and `write`.
Verify: the embedding arrays have `embeddingDimension` entries.

## Checked

2026-11-02. Confirmed in the FastRP page and the running-algorithms page. Removed: the `mutateProperty` example, vector-index step and cosine remark (not read).
Method: documentation only; no commands were run.
