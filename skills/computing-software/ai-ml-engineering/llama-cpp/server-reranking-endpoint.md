---
id: computing-software.ai-ml-engineering.llama-cpp.server-reranking-endpoint
name: server-reranking-endpoint
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, reranking, rerank-endpoint, ubatch-size, jina-format]
level: practitioner
status: docs-checked
description: "Enable and call the rerank endpoint: required flags, TEI versus Jina request shapes, scores and size limits."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# POST /reranking

A rerank model (for example bge-reranker-v2-m3) is required, with either `--reranking` or `--embedding --pooling rank`. The endpoint is not OAI-compatible. Aliases: `/rerank`, `/v1/rerank`, `/v1/reranking`.

The request key that carries the documents picks the format:

- `texts` (TEI format): `query` plus `texts`; set `return_text: true` to echo the text. Response is a bare array of `{index, score}`.
- `documents` (Jina format): supports multimodal items. Response is an object with `model`, `object`, `usage` and `results` of `{index, relevance_score}`.

```bash
curl http://127.0.0.1:8012/v1/rerank -H "Content-Type: application/json" -d '{
  "query": "What is machine learning?",
  "texts": ["Machine learning is a subset of artificial intelligence.",
            "A python is a large snake."],
  "return_text": true }'
```

Other options: `top_n` (default all) and `model`. Results are sorted by descending score and cut to `top_n`; the score is a match probability in [0, 1]. For multimodal rerankers such as Qwen3-VL-Reranker, `query` and documents may be objects `{"text": ..., "image": url | data-uri | base64}`; images never appear in responses.

Input size: a bidirectional-encoder reranker (bge-reranker-v2-m3) must fit the whole prompt within `--ubatch-size`, so raise it if inputs are large. Causal decoder rerankers have no such limit.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: required model and flags, the aliases, TEI versus Jina selection by key, response shapes, top_n, return_text, model, multimodal object form, score range, sort and truncation, and the ubatch-size note. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
