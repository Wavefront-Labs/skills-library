---
id: computing-software.ai-ml-engineering.ml-platform-engineering.llm-inference-slos-ttft-and-throughput
name: llm-inference-slos-ttft-and-throughput
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, gpu-monitoring, ttft, inference-slo, tpot, goodput, vllm-metrics, llm-serving]
level: practitioner
status: draft
description: "Define and monitor LLM serving SLOs: time to first token, time per output token, queue depth and KV-cache usage from vLLM/TGI metrics, and capacity planning against them."
sources:
  - https://docs.vllm.ai/en/latest/serving/metrics.html
  - https://huggingface.co/docs/text-generation-inference/en/reference/metrics
  - https://arxiv.org/abs/2401.09670
  - https://sre.google/sre-book/service-level-objectives/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LLM inference SLOs: TTFT, TPOT and throughput

**Goal:** set latency targets that reflect user experience for streaming LLM responses, and alert/scale on them.

## The metrics
- **TTFT (time to first token):** request arrival to first streamed token. Dominated by queueing + prefill (prompt length). Users perceive this as "responsiveness".
- **TPOT / ITL (time per output token / inter-token latency):** decode speed. 30-50 ms/token reads faster than people read.
- **End-to-end latency** = TTFT + TPOT x output tokens. Use it for non-streaming APIs.
- **Throughput:** output tokens/s across the server. Raising batch size raises throughput but also TPOT.
- **Goodput:** requests/s that meet *both* TTFT and TPOT SLOs (DistServe paper) - the number to maximise, not raw throughput.

## Where to read them
vLLM Prometheus endpoint (`/metrics`):
- `vllm:time_to_first_token_seconds` (histogram), `vllm:time_per_output_token_seconds`, `vllm:e2e_request_latency_seconds`
- `vllm:num_requests_running`, `vllm:num_requests_waiting` (queue)
- `vllm:gpu_cache_usage_perc` (KV-cache fill), `vllm:num_preemptions_total`
TGI exposes similar `tgi_request_*` histograms and queue size.

Example SLO queries:
```
histogram_quantile(0.95, sum by (le) (rate(vllm:time_to_first_token_seconds_bucket[5m]))) < 1.0
histogram_quantile(0.95, sum by (le) (rate(vllm:time_per_output_token_seconds_bucket[5m]))) < 0.05
```

## Setting SLOs
- Separate SLOs per traffic class: interactive chat (p95 TTFT < 1 s), agents/tools (TPOT matters more), batch (throughput only).
- Prompt length drives TTFT: report TTFT bucketed by input tokens, or long-context requests will dominate p95 and hide regressions on normal requests.

## Scaling signals
- `num_requests_waiting > 0` sustained or rising TTFT -> add replicas (prefill-bound/queueing).
- KV cache near 100% with preemptions rising -> requests are being evicted and recomputed; lower `max_num_seqs`, enable prefix caching, or add memory/replicas.
- CPU-style utilisation metrics are misleading for LLM servers; autoscale on queue depth or TTFT, not GPU util.

## Verify
- [ ] TTFT and TPOT p50/p95 on a dashboard, split by route and input-length bucket.
- [ ] Load test with a realistic prompt/output length distribution finds the max goodput per replica.
- [ ] Alerts on SLO burn rate, not single spikes.
