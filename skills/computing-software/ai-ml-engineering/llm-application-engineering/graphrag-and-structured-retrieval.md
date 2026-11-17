---
id: computing-software.ai-ml-engineering.llm-application-engineering.graphrag-and-structured-retrieval
name: graphrag-and-structured-retrieval
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, rag, graphrag, knowledge-graph, community-summaries, text-to-cypher, structured-retrieval]
level: practitioner
status: draft
description: "Decide when graph-based retrieval beats chunk RAG and build it: Microsoft GraphRAG indexing and global/local search, knowledge-graph text-to-Cypher, costs and pitfalls."
sources:
  - https://arxiv.org/abs/2404.16130
  - https://microsoft.github.io/graphrag/
  - https://neo4j.com/docs/cypher-manual/current/introduction/
  - https://python.langchain.com/docs/tutorials/graph/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GraphRAG and structured retrieval

**Goal:** answer questions that need connections across many documents ("what are the main themes", "which suppliers are linked to these incidents") where top-k chunk retrieval fails.

## When chunk RAG is not enough
- **Global questions** about a whole corpus (summaries, themes): no single chunk contains the answer.
- **Multi-hop** questions across entities: A works with B, B supplies C.
- **Aggregations** (counts, filters over attributes): better served by structured queries than by text retrieval.

## Microsoft GraphRAG
Pipeline (Edge et al., 2024): LLM extracts entities and relationships from chunks -> builds a graph -> Leiden community detection at several levels -> LLM writes a summary per community.
```bash
pip install graphrag
graphrag init --root ./proj          # writes settings.yaml and prompts
# put .txt files in ./proj/input, set the API key in .env
graphrag index --root ./proj
graphrag query --root ./proj --method global --query "What are the main risk themes?"
graphrag query --root ./proj --method local  --query "Who supplies Acme's sensors?"
```
- **Global search** map-reduces over community summaries: good for corpus-wide questions.
- **Local search** starts from matched entities and expands to neighbours plus their source text: good for entity questions.
- Tune the extraction prompts to your domain (`graphrag prompt-tune`); generic prompts extract generic entities.
- Indexing cost: many LLM calls per chunk. Run on a sample first and extrapolate tokens/cost before indexing everything; use a cheaper model for extraction.

## Knowledge graph + text-to-query
If you already have structured data (CRM, CMDB, product catalogue), load it into a graph DB (Neo4j) or keep it relational, and have the LLM write queries:
- Give the schema (labels, relationship types, properties) in the prompt; few-shot examples of question -> Cypher.
- Validate queries before execution (read-only user, `EXPLAIN`, deny write clauses), cap result size, and retry on syntax errors with the error message.
- Combine: route aggregation/relationship questions to the graph query and descriptive questions to vector search.

## Pitfalls
- Entity resolution: "IBM", "I.B.M." and "International Business Machines" become three nodes unless you normalise; duplicated nodes break multi-hop answers.
- Graphs go stale; plan incremental re-indexing (GraphRAG supports updating an index) and track source versions.
- Evaluate against plain RAG on your own question set; for many fact-lookup workloads plain hybrid search wins on cost and accuracy.

## Verify
- [ ] Question set split into global / multi-hop / lookup, and each method scored on each.
- [ ] Index cost estimated from a sample before full run.
- [ ] Generated graph queries execute with read-only credentials.
