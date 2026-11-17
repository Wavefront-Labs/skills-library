---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-metrics-dashboards
name: llm-metrics-dashboards
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-metrics-dashboard, observability, opentelemetry, grafana, token-usage]
level: practitioner
status: draft
description: "Build LLM operations dashboards: request, error, latency and TTFT panels, token and cost breakdowns, cache hit ratio, stop reasons and quality scores, with alert thresholds."
sources:
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/
  - https://docs.claude.com/en/docs/build-with-claude/prompt-caching
  - https://grafana.com/docs/grafana/latest/dashboards/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# LLM metrics dashboards

**Goal:** one screen tells on-call whether the LLM feature is healthy and one tells the product owner what it costs and how good it is.

## Emit the data
Per LLM call, record: route/feature, model, provider, status (ok, 429, 5xx, timeout), `stop_reason`, input tokens, output tokens, cache read and cache write tokens, TTFT, total duration, tool calls count, cost, tenant, prompt version. OpenTelemetry GenAI semantic conventions define `gen_ai.client.token.usage` and `gen_ai.client.operation.duration` histograms with attributes such as `gen_ai.request.model` and `gen_ai.operation.name`; use them so any backend can chart the data.

## Operations dashboard
| Panel | Query idea |
|---|---|
| Requests/s by route | rate of calls |
| Error rate by type | 429 vs 5xx vs timeout vs refusal |
| Latency p50/p95, TTFT p95 | histogram quantiles |
| Stop reasons | share of `max_tokens` (truncation) and `refusal` |
| Retries and fallbacks | count of fallback model use |
| Rate-limit headroom | tokens/min vs limit |
```
histogram_quantile(0.95, sum by (le, route) (rate(gen_ai_client_operation_duration_seconds_bucket[5m])))
sum by (gen_ai_token_type) (rate(gen_ai_client_token_usage_sum{route="support"}[1h]))
```

## Cost and efficiency dashboard
- Cost per day by feature, model and tenant; cost per request and per completed task.
- Tokens per request trend (catches runaway prompts and agent loops).
- **Cache hit ratio** = cache_read / (cache_read + cache_write + uncached input). A drop after a deploy usually means a prompt-prefix change invalidated caching.
- Batch vs real-time share.

## Quality dashboard
Online judge scores, user feedback rate (thumbs up/down), escalation-to-human rate, guardrail trigger rates - by prompt version and model, with deploy annotations.

## Alerts
- Error rate > 2% for 5 min; 429s sustained.
- p95 latency over SLO.
- `max_tokens` stop rate > baseline x 2.
- Daily cost > forecast x 1.3; tokens per request jump.
- Cache hit ratio drops by more than 20 points.
- Quality score drop beyond its confidence interval.

## Verify
- [ ] Every panel filterable by route, model and prompt version.
- [ ] Deploy markers on all time series.
- [ ] Alerts tested and linked to runbooks.
