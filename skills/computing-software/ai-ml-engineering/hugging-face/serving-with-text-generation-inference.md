---
id: computing-software.ai-ml-engineering.hugging-face.serving-with-text-generation-inference
name: serving-with-text-generation-inference
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, quantization, text-generation-inference, tgi, llm-serving, messages-api, continuous-batching]
level: practitioner
status: docs-checked
description: "Serve LLMs with Hugging Face TGI: Docker launch, token limits and batching flags, quantization and sharding, OpenAI-compatible Messages API, metrics and sizing."
sources:
  - https://huggingface.co/docs/text-generation-inference/en/quicktour
  - https://huggingface.co/docs/text-generation-inference/en/reference/launcher
  - https://huggingface.co/docs/text-generation-inference/en/messages_api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving with Text Generation Inference (TGI)

**Goal:** a production LLM endpoint with continuous batching, streaming and an OpenAI-compatible API. (Check the TGI repository for current maintenance status; vLLM and SGLang are the common alternatives with similar flags.)

## Launch
```bash
model=meta-llama/Llama-3.1-8B-Instruct
docker run --gpus all --shm-size 1g -p 8080:80 -v $PWD/data:/data \
  -e HF_TOKEN=$HF_TOKEN \
  ghcr.io/huggingface/text-generation-inference:<version> \
  --model-id $model \
  --max-input-tokens 8000 --max-total-tokens 8192 \
  --max-batch-prefill-tokens 8192 \
  --num-shard 1
```
- Mount `/data` so weights are cached across restarts.
- `--max-total-tokens` = input + output per request; with `--max-batch-prefill-tokens` see the launcher reference for exactly what each limits; lower them or add shards if the model does not fit.
- `--num-shard N` tensor-parallel across N GPUs.
- `--quantize awq|gptq|bitsandbytes-nf4|eetq` (the launcher reference lists more, such as marlin and exl2) (pre-quantized checkpoints are detected automatically).

## Call it
```bash
curl localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "tgi", "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 128, "stream": true}'
```
The OpenAI Python client works with `base_url="http://host:8080/v1"`. Native endpoints for non-chat use: `/generate`, `/generate_stream`.

## Operate
- TGI exports Prometheus metrics; the monitoring tutorial in the TGI docs points to a Grafana dashboard template (`tgi_grafana.json`).
- Autoscale on queue depth / TTFT rather than GPU utilisation.
- Set request timeouts and `max_new_tokens` caps at the gateway to protect the batch from huge requests.

## Gotchas
- The quicktour's Docker command passes `--shm-size 1g`; keep it.
- Pin the image version; flags and defaults change between releases.

## Verify
- [ ] Load test with realistic prompt/output lengths: p95 TTFT and tokens/s meet targets.
- [ ] Streaming works through your gateway/proxy (no response buffering).
- [ ] Server starts and serves a request at the configured token limits.

## Checked
Date: 2026-10-28.
- Confirmed in the TGI launcher reference: `--num-shard`, `--quantize` values awq, gptq, eetq, bitsandbytes-nf4 (pre-quantized models need no flag), `--max-input-tokens`, `--max-total-tokens`, `--max-batch-prefill-tokens`. Quicktour: `--shm-size 1g`, `/data` volume. Consuming-TGI tutorial: `/generate`, `/generate_stream`, OpenAI client `base_url` with `/v1`. Monitoring tutorial: Prometheus and `tgi_grafana.json`.
- Removed as unconfirmed: `fp8` quantize value, `/health` `/info` `/metrics` route names, grammar/response_format, startup KV-cache check, server-side chat template sentence, NCCL and gated-model gotchas.
Method: documentation only; no commands were run.
