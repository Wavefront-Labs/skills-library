---
id: computing-software.database-administration.neo4j.entity-extraction-loading
name: entity-extraction-loading
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, entity-extraction, kg-builder, schema-guided-extraction, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Build a Neo4j knowledge graph from text with SimpleKGPipeline: chunking, embeddings, schema modes, lexical graph, entity resolvers"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://github.com/neo4j/neo4j-graphrag-python/blob/main/docs/source/user_guide_kg_builder.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a knowledge graph from text

Goal: ingest documents as a graph with the `neo4j-graphrag` KG builder.

- The pipeline stages are: data loader, text splitter, optional chunk embedder, schema builder, optional lexical graph builder, entity and relation extractor, graph pruner, KG writer, entity resolver.
- Fastest start: `SimpleKGPipeline(llm=..., driver=..., embedder=..., from_file=True)` then `await kg_builder.run_async(file_path=...)` (use `text=` with `from_file=False`).
- Chunking: swap in a `FixedSizeSplitter(chunk_size=..., chunk_overlap=...)` to fit the LLM context window.
- Schema grounding via the `schema` parameter: `EXTRACTED` (default; the LLM derives one schema from the input text and uses it for all chunks), `FREE` (no schema, unguided extraction), or a schema you supply. A schema can be saved to and reloaded from JSON or YAML. Structured output mode enforces schema conformance for supported LLMs.
- The lexical graph holds a `Document` node (with `path`), `Chunk` nodes (with `text` and, if computed, `embedding`), `FROM_DOCUMENT` links from each chunk to its document and `NEXT_CHUNK` links between consecutive chunks. Chunk nodes also record `embedding_model_name`; update it if you re-embed with another model.
- `on_error` is `RAISE` or `IGNORE`.
- Deduplicate with an entity resolver: `SinglePropertyExactMatchResolver` (same label and identical `name`), `SpaCySemanticMatchResolver` (embedding cosine similarity) or `FuzzyMatchResolver` (RapidFuzz, faster but less precise). These replace the nodes the KG writer created, and the last two need extra dependencies.

Verify: spot-check extracted relations against the source text.

## Checked
2026-11-09

Method: read the neo4j-graphrag-python user guide for the KG builder (raw rst: pipeline structure, SimpleKGPipeline, lexical graph, schema, entity resolver). Removed: unsupported advice to MERGE on unique keys with constraints and the claim of chunk-to-entity provenance edges (guide documents only the Document/Chunk relationships). Not checked: the YAML/JSON pipeline config and the graph pruner details.
