---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.embed-and-compare-text
name: embed-and-compare-text
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [embeddings, embed, embedmany, cosine-similarity, rag, vector]
level: practitioner
status: docs-checked
description: "Embed one or many strings with embed and embedMany, compare vectors with cosineSimilarity, and tune dimensions, parallelism, retries and defaults."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/embeddings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn text into vectors with the AI SDK and rank or cluster them by similarity.

1. Single value: `const { embedding, usage, response } = await embed({ model: 'openai/text-embedding-3-small', value: 'sunny day at the beach' })`. `embedding` is a `number[]`; `usage` is for example `{ tokens: 10 }`; `response` is the raw provider response.
2. Many values (data loading for RAG): `const { embeddings, usage } = await embedMany({ model, values: [...] })`. `embeddings` is `number[][]` in the same order as `values`.
3. Compare: `import { cosineSimilarity } from 'ai'; cosineSimilarity(embeddings[0], embeddings[1])`. Use it to rank or filter items by similarity.
4. Models can be a gateway string id or a provider instance such as `openai.embedding('text-embedding-3-small')` (the page also spells it `openai.embeddingModel(...)`).

Settings shared by `embed` and `embedMany`:
- `dimensions`: positive integer requesting an output vector size. Omitted means the model default. `embedMany` forwards the same value to every batch. The SDK does not truncate or resize; support depends on the model. An explicit dimension in `providerOptions` (for example `providerOptions: { openai: { dimensions: 512 } }`) takes precedence over the top-level `dimensions`.
- `maxRetries`: defaults to 2 retries (3 attempts); 0 disables retries.
- `abortSignal` (for example `AbortSignal.timeout(1000)`) and `headers`.
- `embedMany` only: `maxParallelCalls` limits parallel batch requests.

Default settings for every call: wrap the model.

```ts
const m = wrapEmbeddingModel({
  model: gateway.embeddingModel('google/gemini-embedding-001'),
  middleware: defaultEmbeddingSettingsMiddleware({
    settings: { providerOptions: { google: { outputDimensionality: 256, taskType: 'CLASSIFICATION' } } },
  }),
});
```

Gotchas:
- Embedding dimensions differ by model. Listed sizes: text-embedding-3-large 3072, text-embedding-3-small 1536, mistral-embed 1024.
- Google `gemini-embedding-2` is multimodal via `providerOptions.google.content`; each entry matches the value at the same index and holds `{ text }`, `{ inlineData: { mimeType, data } }` or `{ fileData: { fileUri, mimeType } }`.
- Many providers charge by tokens used; both `embed` and `embedMany` return this in `usage` (for example `{ tokens: 10 }`).

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the "vectors from different models not comparable" claim and the usage.tokens logging advice; restated usage as the docs show it.

Method: documentation only; no commands were run.
