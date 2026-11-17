---
id: computing-software.ai-ml-engineering.mastra.setup-semantic-recall
name: setup-semantic-recall
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, memory, semanticrecall, embedder, vector, metadata-filter, fastembed, pgvector]
level: practitioner
status: docs-checked
description: "Enable Mastra semantic recall: vector store and embedder, topK/messageRange/scope/filter options, server-side embeddings, FastEmbed, embeddingDimension and PgVector HNSW."
sources:
  - https://mastra.ai/docs/memory/semantic-recall
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let a Mastra agent retrieve earlier messages by meaning, from its thread or all of a user's threads.

## How it works
Before the LLM call, the user prompt is embedded and a vector DB is queried; the hits join the context. After the response, all new messages (user, assistant, tool calls/results) are embedded and inserted. It is off by default and adds latency per call. Leave it off when message history is enough or for latency-sensitive uses such as realtime two-way audio.

## Quickstart
Set `semanticRecall: true`, plus a `vector` store and an `embedder`:

```typescript
memory: new Memory({
  storage: new LibSQLStore({ id: 'agent-storage', url: 'file:./local.db' }),
  vector: new LibSQLVector({ id: 'agent-vector', url: 'file:./local.db' }),
  embedder: new ModelRouterEmbeddingModel('openai/text-embedding-3-small'),
  options: { semanticRecall: true },
})
```
`ModelRouterEmbeddingModel` is from `@mastra/core/llm`. The page also shows MongoDB (`MongoDBStore`, `MongoDBVector`) and lists vector stores including Astra, Chroma, Pinecone, PostgreSQL, Qdrant, Upstash and others.

## Recall options
```typescript
semanticRecall: {
  topK: 3,            // similar messages to retrieve
  messageRange: 2,    // messages before and after each match
  scope: 'resource',  // search all threads for the resource
  filter: { projectId: { $eq: 'project-a' } },
}
```
`scope: 'resource'` is supported by the LibSQL, OracleDB, PostgreSQL, MongoDB and Upstash adapters.

## Metadata filters
`filter` matches metadata stored on message embeddings when messages are saved; if thread metadata changes later, existing embeddings keep the old metadata until re-saved or re-indexed. Operators: `$and`, `$or`, `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`. Example: `{ $and: [{ projectId: { $eq: 'project-a' } }, { priority: { $gte: 3 } }] }`.

## Manual recall
`const memory = await agent.getMemory()` then `memory!.recall({ threadId, vectorSearchString: '...', threadConfig: { semanticRecall: true } })`; without the search string it behaves like `listMessages` (use `perPage`).

## Embedders
- Model router: `openai/text-embedding-3-small` (also `-3-large`, `ada-002`), Google `gemini-embedding-001`, or OpenRouter via `new ModelRouterEmbeddingModel({ providerId: 'openrouter', modelId: 'openai/text-embedding-3-small' })`. Keys are detected from `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `OPENROUTER_API_KEY` (Google also falls back to `GOOGLE_GENERATIVE_AI_API_KEY`).
- Local FastEmbed: `npm install @mastra/fastembed@latest`, then `embedder: fastembed`. For non-English, `fastembed.multilingualE5LargePassage` (use one model consistently; Memory uses one embedder for storing and recalling; 1024 dimensions, cannot mix with another embedder's vectors in one index). FastEmbed truncates inputs past 512 tokens, so chunk long documents (for example `maxSize: 1500` in `MDocument.chunk()`).
- Server-side embeddings: with MongoDB Automated Embedding, set `autoEmbed: { model: 'voyage-4' }` on `MongoDBVector` and omit `embedder`; new messages embed in the background so a just-saved message may not be recallable yet. Enabling semantic recall with neither an embedder nor a server-side-embedding store raises an error.

## embeddingDimension
Memory probes the embedder once per instance to learn the dimension. Set `embeddingDimension: 1536` (for `openai/text-embedding-3-small`) to skip the probe. On mismatch with real vectors it throws `MASTRA_MEMORY_EMBEDDING_DIMENSION_MISMATCH`; update it whenever the model changes.

## PostgreSQL index
Default is IVFFlat; HNSW is typically faster. PgVector uses the index for thread/resource-filtered searches only with HNSW on pgvector 0.8.0 or newer.
```typescript
semanticRecall: { topK: 5, messageRange: 2, indexConfig: { type: 'hnsw', metric: 'dotproduct', hnsw: { m: 16, efConstruction: 64 } } }
```

## Debugging
With tracing enabled, recalled messages appear in the agent trace alongside recent history.

## Checked
Method: 2026-11-08 read the cited Mastra semantic-recall page in full (served as markdown) and compared each claim. All claims matched; no content changes.
