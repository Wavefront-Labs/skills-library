---
id: computing-software.ai-ml-engineering.kserve.kserve-data-plane-components
name: kserve-data-plane-components
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [data-plane, predictor, transformer, explainer, traffic-flow, explain, predict, openai-compatible, v1chatcompletions, v1embeddings]
level: practitioner
status: docs-checked
description: "KServe data plane: predictor, optional transformer and explainer, request flow, and the OpenAI-compatible endpoints used for generative inference."
sources: ["https://github.com/kserve/website/blob/main/docs/concepts/architecture/data-plane/data-plane.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KServe data plane components and protocols

An InferenceService endpoint is a static graph of up to three components; only the **predictor** is required.

- **Predictor**: loads the model from storage and serves it (resource management, protocol handling).
- **Transformer** (optional): pre/post-processing, feature engineering (for example Feast), schema validation.
- **Explainer** (optional): same API as predict but with the `:explain` verb; calls the predictor internally (TrustyAI, Alibi).
- Gateway: routing, load balancing, traffic splitting for canary/A-B.

Request flow: client -> gateway -> transformer (pre-process) -> predictor (`:predict`) -> transformer (post-process) -> client. For explain: transformer -> explainer -> predictor -> explainer -> transformer.

## Protocol choice for predictive models
V1 (HTTP/REST, TensorFlow-Serving style, has `:explain`) or V2 / Open Inference Protocol (REST + gRPC, `/infer` instead of `:predict`, server ready/live/metadata endpoints, optional model version in path, no explain).

## Generative inference
OpenAI-compatible endpoints with SSE streaming:

| API | Method and path |
|---|---|
| Chat completion | POST /v1/chat/completions |
| Completion | POST /v1/completions |
| Embeddings | POST /v1/embeddings |
| Score (not in OpenAI spec) | POST /v1/score |

The generative architecture adds Envoy AI Gateway (auth, rate limiting, usage tracking), the Gateway API Inference Extension endpoint picker (load- and cache-aware routing), vLLM containers, and distributed head/worker or prefill/decode deployments.

## Checked

Checked 2026-11-08 against the KServe website page data-plane.md, read in full: predictor, transformer, explainer and gateway roles, the predict and explain request flows, V1 versus V2 differences, the OpenAI-compatible endpoint table including the non-OpenAI score API, and the generative component list. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
