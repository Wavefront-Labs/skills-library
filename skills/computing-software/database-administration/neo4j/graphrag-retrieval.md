---
id: computing-software.database-administration.neo4j.graphrag-retrieval
name: graphrag-retrieval
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, graph-rag, vector-plus-graph, retrieval-cypher, graphrag, knowledge-graph, neo4j-genai, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "GraphRAG with neo4j-graphrag: VectorRetriever, VectorCypherRetriever retrieval queries, hybrid retrievers, return_context"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://github.com/neo4j/neo4j-graphrag-python/blob/main/docs/source/user_guide_rag.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphRAG retrieval

Goal: retrieve graph-aware context for an LLM with the `neo4j-graphrag` Python package.

- A GraphRAG query needs three parts: a Neo4j driver, a retriever and an LLM (`GraphRAG(retriever=..., llm=...)`, then `rag.search(query_text=..., retriever_config={"top_k": 5})`).
- `VectorRetriever(driver, index_name, embedder)` runs a similarity search on a Neo4j vector index and returns the matched node and score. The index uses approximate nearest neighbour, so check the vector index limitations in the Cypher manual.
- To expand from the seed nodes use `VectorCypherRetriever` with a `retrieval_query`. The query runs after the index search with `node` (the match) and `score` in scope, for example `RETURN node.title AS movieTitle, collect { MATCH (a:Actor)-[:ACTED_IN]->(node) RETURN a.name } AS actors`. The guide recommends returning node properties, not nodes. A `result_formatter` (beta API) turns each record into content plus metadata for the prompt.
- Other retrievers: `HybridRetriever` and `HybridCypherRetriever` (vector plus full-text index), `Text2Cypher`, `ToolsRetriever`, and variants for vectors held in Weaviate, Pinecone or Qdrant.
- Pass `return_context=True` to `rag.search` to see what was retrieved.

Verify: with `return_context=True`, check the answer is supported by the returned nodes.

## Checked
2026-11-09

Method: read the neo4j-graphrag-python user guide for RAG (raw rst, retriever sections and quickstart). Removed: the unsupported "keep retrieval queries parameterised and bounded" advice (not in the guide) and the "confirm" hedge on retrievers (confirmed). Not checked: the ToolsRetriever and external vector database sections in detail, or the Cypher-manual vector index limitations page.
