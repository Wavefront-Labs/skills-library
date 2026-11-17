---
id: computing-software.ai-ml-engineering.mlops.vllm-offline-batch-inference
name: vllm-offline-batch-inference
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, vllm-offline-inference, vllm, batch-inference, llm-batch, sampling-params, throughput]
level: practitioner
status: draft
description: "Run large offline LLM jobs with vLLM's LLM class: SamplingParams, chat batches, tensor parallelism, structured outputs, prefix caching, Ray Data scaling and checkpointed outputs."
sources:
  - https://docs.vllm.ai/en/latest/serving/offline_inference.html
  - https://docs.vllm.ai/en/latest/api/vllm/index.html
  - https://docs.ray.io/en/latest/data/working-with-llms.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Offline LLM batch inference with vLLM

**Use for:** classifying, extracting or generating over millions of records with open-weight models at maximum throughput (no HTTP server needed).

## Basic job
```python
from vllm import LLM, SamplingParams
llm = LLM(model="Qwen/Qwen2.5-7B-Instruct", dtype="bfloat16", tensor_parallel_size=1,
          max_model_len=8192, gpu_memory_utilization=0.90, enable_prefix_caching=True)
params = SamplingParams(temperature=0.0, max_tokens=256, stop=["</answer>"])
conversations = [[{"role": "system", "content": SYSTEM}, {"role": "user", "content": doc}] for doc in docs]
outputs = llm.chat(conversations, params, use_tqdm=True)
results = [o.outputs[0].text for o in outputs]       # same order as inputs
```
- Submit large lists at once; vLLM's continuous batching schedules them. Do not loop one prompt at a time.
- Prefix caching speeds up shared system prompts/few-shot prefixes.
- Structured output: `SamplingParams(guided_decoding=GuidedDecodingParams(json=schema))` (name varies by version: `structured_outputs` in newer releases).

## Sizing
- `tensor_parallel_size` = GPUs per model replica (needed when weights + KV cache exceed one GPU). For throughput with a model that fits on one GPU, run one replica per GPU instead (data parallel).
- `max_model_len` lower = more KV cache room = bigger batches.
- Quantized checkpoints (FP8/AWQ) increase throughput per GPU.

## Scale out and resilience
- Ray Data LLM processors (`ray.data.llm`) shard a dataset across many vLLM replicas with backpressure.
- Process in chunks (e.g. 50k rows), write each chunk's outputs to Parquet with input ids, and skip completed chunks on restart: idempotent and resumable.
- Validate outputs per row (parse JSON, check labels); re-queue failures with a retry prompt.

## Cost check
Measure tokens/s on a 1k-row sample, extrapolate GPU-hours, and compare with provider batch APIs (often 50% discount) before committing.

## Verify
- [ ] Output count equals input count; parse failure rate below threshold; spot-check quality on a labeled sample.
