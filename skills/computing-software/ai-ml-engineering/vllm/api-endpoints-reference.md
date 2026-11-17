---
id: computing-software.ai-ml-engineering.vllm.api-endpoints-reference
name: api-endpoints-reference
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [endpoints, metrics-endpoint, enable-offline-docs, scale-out, load-lora-adapter]
level: practitioner
status: docs-checked
description: "List the HTTP endpoint families vllm serve exposes, including instrumentator, LoRA, profiling and scale-out APIs."
sources:
  - https://docs.vllm.ai/en/latest/serving/online_serving/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know which endpoints a vLLM server exposes beyond the OpenAI core.

OpenAI core: `/v1/completions` (no `suffix`), `/v1/chat/completions` (needs a chat template; `user` ignored; `parallel_tool_calls=false` limits to zero or one call), `/v1/chat/completions/batch`, `/v1/responses` (plus get and cancel by id), `/v1/embeddings`, `/v1/audio/transcriptions`, `/v1/audio/translations`, `/v1/decisions`.

Other API families: Anthropic messages (`/v1/messages`, `/v1/messages/count_tokens`); Cohere Embed (`/v2/embed`) and Rerank (`/rerank`, `/v1/rerank`, `/v2/rerank`); pooling endpoints `/classify`, `/score` and `/v1/score`, and `/pooling`; speech-to-text including `/v1/realtime`; `/generative_scoring` (next-token probabilities for `label_token_ids`); `/v1/systemone` (typed questions with a probability per allowed answer).

Instrumentator endpoints:
- `/version`, `/load`, `/v1/models`, `/health`
- `/metrics` Prometheus-compatible
- `/start_profile` and `/stop_profile`; the start call accepts an optional JSON body with `profiler_kwargs`
- `/ping` and `/invocations` (SageMaker-compatible, same functions as `/v1`)
- `/tokenize`, `/detokenize`, `/tokenizer_info`
- `/scale_elastic_ep` and `/is_scaling_elastic_ep` for elastic expert parallelism

The FastAPI `/docs` page needs internet access by default; for air-gapped use start with `--enable-offline-docs`.

LoRA dynamic loading is enabled in the API server through `/v1/load_lora_adapter` and `/v1/unload_lora_adapter`. The page says this should ONLY be used for local development (the LoRA page separately gates it behind `VLLM_ALLOW_RUNTIME_LORA_UPDATING`).

Scale-out APIs are disabled on `vllm serve` unless you set `--enable-scale-out`. They include the Tokens IN to Tokens OUT generate endpoint `/inference/v1/generate` (optional detokenized text via `output_mode`), `/inference/v1/abort_requests`, the renderer endpoints (`/v1/completions/render`, `/v1/chat/completions/render`, `/v1/responses/render`) and derenderer endpoints. `vllm launch render` and `vllm serve --tokens-only` always register the endpoints they need.

Process checkpoint endpoints (`--enable-sleep-mode`): `/checkpoint/prepare` (`?mode=wait|abort|keep`), `/checkpoint/status` (200 prepared, 503 until then, 500 after failure) and `/checkpoint/restore`.

Development mode: `VLLM_SERVER_DEV_MODE=1` enables cache resets (`/reset_prefix_cache`), `/sleep`, `/wake_up`, `/pause`, `/resume`, weight-update, `/collective_rpc` ("extremely dangerous") and `/server_info`. The page warns these must not be used in production.

Chat template: chat requests need a Jinja2 chat template in the tokenizer config, or `--chat-template` with a file path or string; without one chat requests error. Override auto-detected content format (`string` or `openai`) with `--chat-template-content-format`.

## Checked

Method: 2026-11-08 read the vLLM Online Serving page (docs source markdown, serving/online_serving README) in full and compared every endpoint listed.
Changes: added the OpenAI core list, tokenize, elastic EP, renderer, checkpoint and dev-mode endpoints and the chat template rules. The earlier endpoint, scale-out and LoRA claims were unchanged and match the page; the VLLM_ALLOW_RUNTIME_LORA_UPDATING note comes from the LoRA page.
