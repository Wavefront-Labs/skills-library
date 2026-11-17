---
id: computing-software.ai-ml-engineering.llama-cpp.server-embeddings-endpoints
name: server-embeddings-endpoints
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, embeddings, pooling, normalization, embedding-endpoint]
level: practitioner
status: docs-checked
description: "Compare /v1/embeddings, /embedding and /embeddings, the --embedding and --pooling flags and normalization."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Embedding endpoints

Three routes exist:

- `POST /v1/embeddings`: OpenAI-compatible. Requires a model whose pooling is not `none`; embeddings are normalized with the Euclidean norm. Options follow the OpenAI Embeddings API. For multimodal models (loaded with `--mmproj`) each `input` element can be an object with a `content` array of text, `image_url`, `input_audio` or `input_video` parts; each object yields one embedding. The page notes this shape is not part of the OpenAI API.
- `POST /embedding`: not OAI-compatible (use `/v1/embeddings` for OAI clients). Options: `content` (text to process) and `embd_normalize`. It also supports multimodal embeddings.
- `POST /embeddings`: non-OpenAI response format, with the same options and examples as `/v1/embeddings`. Supports all poolings including `--pooling none`, where the response holds unnormalized embeddings for all input tokens; for other poolings only pooled, Euclidean-normalized embeddings are returned.

`embd_normalize` values: `-1` none, `0` max absolute, `1` taxicab, `2` Euclidean/L2, above 2 p-norm. The server flag `--embd-normalize N` defaults to 2.

Server flags:

- `--embedding`, `--embeddings`: restrict the server to the embedding use case; use only with dedicated embedding models (default disabled).
- `--pooling {none,mean,cls,last,rank}`: pooling type; the model default is used if unspecified.
- `--embd-gemma-default`: use the default EmbeddingGemma model (can download weights from the internet).

```bash
llama-server -m /path/to/embedding-model.gguf --embedding --pooling mean
```

## Checked

Date: 2026-11-08. Confirmed against the /embedding, /embeddings, /v1/embeddings and server-flag entries of the llama-server README. Added the multimodal input shape and the `--embd-normalize` default.

Method: docs-only read of cited pages, 2026-11-08
