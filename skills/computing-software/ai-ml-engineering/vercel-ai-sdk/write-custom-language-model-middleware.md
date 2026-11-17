---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.write-custom-language-model-middleware
name: write-custom-language-model-middleware
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [middleware, languagemodelv4middleware, wrapgenerate, wrapstream, transformparams, guardrails, logging]
level: advanced
status: docs-checked
description: "Implement LanguageModelV4Middleware with transformParams, wrapGenerate and wrapStream for logging, caching, RAG injection and streaming-safe guardrails."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/middleware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write your own middleware object and apply it with `wrapLanguageModel({ model, middleware })`.

Shape (types from `@ai-sdk/provider`): every `LanguageModelV4Middleware` must set `specificationVersion: 'v4'` and may implement:
1. `transformParams({ params })`: modify params before `doGenerate` and `doStream`; return params.
2. `wrapGenerate({ doGenerate, params })`: call `doGenerate()`, return the (possibly modified) result.
3. `wrapStream({ doStream, params })`: `const { stream, ...rest } = await doStream();` return `{ stream: stream.pipeThrough(new TransformStream(...)), ...rest }`.

Patterns from the docs (illustrative, not production):
- Logging: in `wrapGenerate`, collect `result.content.filter(p => p.type === 'text').map(p => p.text).join('')`. In `wrapStream`, track `LanguageModelV4StreamPart` chunks `text-start`, `text-delta` (field `delta`, keyed by `id`), `text-end`, and log in `flush()`.
- Caching: in `wrapGenerate({ doGenerate, params, model })`, key on `JSON.stringify({ provider: model.provider, modelId: model.modelId, params })` so responses are only reused for the same model and request, and return the stored result on a hit. The docs example caches only `wrapGenerate`; streaming caching is left to you.
- RAG: in `transformParams`, read the last user message from `params.prompt`; if none return `params` unchanged, otherwise append retrieved sources as text to the last user message. Helpers like `getLastUserMessageText`, `findSources`, `addToLastUserMessage` are not SDK functions.
- Guardrails: in `wrapGenerate`, map `result.content` and redact text parts. In `wrapStream`, keep a `Map` of buffers per text block id: suppress `text-delta`, and on `text-end` emit one redacted `text-delta` then the `text-end`; on `flush` emit leftovers.

Gotchas:
- Do not redact each streamed delta independently: a match split across deltas leaks. Buffering per text block until `text-end` delays output and uses memory proportional to block size; a fixed-size buffer alone is unsafe for unbounded variable-length patterns.
- Per-request metadata: pass `providerOptions: { yourLogMiddleware: { hello: 'world' } }` to the call and read `params?.providerMetadata?.yourLogMiddleware` inside the middleware (the docs example reads it this way).
- The docs call this advanced functionality that requires a solid understanding of the v4 language model specification.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Corrected the cache key to include provider and modelId, and restated the specification gotcha to the docs wording.

Method: documentation only; no commands were run.
