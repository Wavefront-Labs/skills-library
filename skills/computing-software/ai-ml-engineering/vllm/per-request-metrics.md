---
id: computing-software.ai-ml-engineering.vllm.per-request-metrics
name: per-request-metrics
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [per-request-metrics, enable-per-request-metrics, ttft, queue-time, mean-itl]
level: intro
status: docs-checked
description: "Return timing metrics inside API responses with --enable-per-request-metrics."
sources:
  - https://docs.vllm.ai/en/latest/features/per_request_metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get per-request timings in the response body for billing, SLA monitoring and latency analysis, alongside the aggregated Prometheus metrics at `/metrics`.

Enable it:

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --enable-per-request-metrics
```

Responses then carry a `metrics` object next to `usage`:
- `time_to_first_token_ms`: from scheduling until the first output token.
- `generation_time_ms`: decode time, first to last output token, excluding queue and prefill.
- `queue_time_ms`: time waiting in the scheduler queue.
- `mean_itl_ms`: mean inter-token latency during decode; `null` for single-token responses.
- `tokens_per_second`: output tokens over the whole interval from scheduling to last token, so it includes prefill.

All fields are `null` if timing data is unavailable.

Caveats:
- Metrics are `null` when `n > 1`, since timing reflects only one sequence; token usage stays accurate.
- vLLM rejects the flag if `--disable-log-stats` is also set, because server-side statistics logging is required (on by default).
- At high concurrency the computation may add non-negligible CPU overhead; benchmark before production.

Endpoints: chat completions, `/v1/completions` (omitted for multiple prompts) and `/v1/responses` (top level, or on the `response.completed` event when streaming; omitted for multi-turn tool-call workflows). With `--per-request-spec-decode-metrics`, acceptance length metrics appear as `metrics.speculative_decoding`, again only for `n == 1`.

Streaming: metrics ride on the final usage chunk, emitted only when the client sets `stream_options.include_usage: true` or the server uses `--enable-force-include-usage`. In the Python client read them with `response.model_extra.get("metrics")`.

## Checked

Method: 2026-11-08 read the per-request metrics page in full. Field definitions, null rules, flag conflict and streaming caveat matched. Added the completions, responses and speculative-decoding endpoint notes.
