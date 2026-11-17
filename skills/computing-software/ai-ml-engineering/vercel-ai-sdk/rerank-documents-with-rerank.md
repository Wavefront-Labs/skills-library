---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.rerank-documents-with-rerank
name: rerank-documents-with-rerank
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [reranking, rerank, cohere, retrieval, topn, rag]
level: practitioner
status: docs-checked
description: "Reorder retrieved strings or JSON objects by relevance to a query with the AI SDK rerank function, limiting results with topN and reading ranking fields."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/reranking
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: improve retrieval by reordering candidate documents with a reranking model instead of relying on embedding distance alone.

```ts
import { rerank } from 'ai';
import { cohere } from '@ai-sdk/cohere';

const { ranking, rerankedDocuments, originalDocuments } = await rerank({
  model: cohere.reranking('rerank-v4.0-pro'),
  documents: ['sunny day at the beach', 'rainy afternoon in the city', 'snowy night in the mountains'],
  query: 'talk about rain',
  topN: 2,
});
```

Result fields:
- `ranking`: sorted array of `{ originalIndex, score, document }`. `score` is typically 0-1, higher is more relevant. `originalIndex` is the position in your input array, so you can map back to database ids.
- `rerankedDocuments`: documents already sorted by relevance (convenience).
- `originalDocuments`: the input array.
- `response`: `{ id, timestamp, modelId, headers, body }`, the raw provider response.

Object documents work too: pass an array of JSON objects (for example `{ from, subject, text }` emails) and `rerankedDocuments[0]` returns the full object.

Options:
- `topN`: return only the N best documents.
- `providerOptions`: for Cohere, `{ cohere: { maxTokensPerDoc: 1000 } }` limits tokens per document.
- `maxRetries`: default 2 retries (3 attempts), 0 disables.
- `abortSignal` (for example `AbortSignal.timeout(5000)`) and `headers`.

Models named on the page: Cohere `rerank-v4.0-pro`, `rerank-v4.0-fast`, `rerank-v3.5`; Amazon Bedrock `amazon.rerank-v1:0` and `cohere.rerank-v3-5:0` (via `bedrock.reranking(...)`); Together.ai `Salesforce/Llama-Rank-v1`, `mixedbread-ai/Mxbai-Rerank-Large-V2`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the "typical pipeline" paragraph (embed plus vector store then topN), which is not on the page.

Method: documentation only; no commands were run.
