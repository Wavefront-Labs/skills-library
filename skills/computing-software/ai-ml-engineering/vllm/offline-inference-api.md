---
id: computing-software.ai-ml-engineering.vllm.offline-inference-api
name: offline-inference-api
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [offline-inference, llm-class, generate, chat, reset-prefix-cache]
level: intro
status: docs-checked
description: "Map the LLM class methods for offline inference: generate, chat, queue, pooling, profiling, sleep and cache calls."
sources:
  - https://docs.vllm.ai/en/latest/serving/offline_inference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right `vllm.LLM` method for offline inference in your own code.

Offline inference runs in your own code through the `LLM` class. Two model types: generative models (LLaMA, Qwen, DeepSeek) and pooling models (classification and retrieval, such as bge-m3 and Qwen3 Reranker).

Generative:
- `LLM.generate` completions for prompts.
- `LLM.chat` responses for a chat conversation.

Asynchronous queue:
- `LLM.enqueue` and `LLM.enqueue_chat` add work without waiting.
- `LLM.wait_for_completion` waits for all enqueued requests and returns results.

Pooling:
- `LLM.classify` classification models only.
- `LLM.embed` embedding models only.
- `LLM.score` cross-encoder, bi-encoder and late-interaction score models.
- `LLM.encode` all pooling models.

Operations:
- `LLM.start_profile(profile_prefix=..., profiler_kwargs=...)` and `LLM.stop_profile`; both arguments are optional.
- `LLM.sleep` and `LLM.wake_up` for sleep mode.
- `LLM.reset_mm_cache` and `LLM.reset_prefix_cache`.
- `LLM.get_metrics` returns a snapshot of aggregated Prometheus metrics.
- `LLM.collective_rpc` runs a method or callable across all workers; `LLM.apply_model` applies a function to the model inside each worker.

RL training weight transfer: `LLM.init_weight_transfer_engine`, `LLM.start_weight_update`, `LLM.update_weights`, `LLM.finish_weight_update`, `LLM.update_weight_version` (sets the weight version without updating weights) and `LLM.get_weight_version` (latest committed version).

Profiling traces are described in the contributing profiling guide. For large-scale offline batches, the page points to Ray Data LLM (`ray.data.llm`, needs ray>=2.44.1), which uses vLLM as the engine and adds streaming execution, sharding, autoscaling and continuous batching.

## Checked

Method: 2026-11-08 read the vLLM Offline Inference page (docs source markdown) in full.
Changes: removed the engine-argument example (`tensor_parallel_size=2` on a granite model) because the page does not show it; added collective_rpc, apply_model, get_weight_version and the Ray Data LLM pointer. Method list otherwise unchanged and matches the page.
