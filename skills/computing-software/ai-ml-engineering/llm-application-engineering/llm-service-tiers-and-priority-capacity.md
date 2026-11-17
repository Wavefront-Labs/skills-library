---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-service-tiers-and-priority-capacity
name: llm-service-tiers-and-priority-capacity
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, service-tiers, priority-tier, batch-api, capacity-planning]
level: practitioner
status: docs-checked
description: "Choose Claude capacity tiers: standard, Priority Tier (legacy commitments) and batch, the service_tier parameter, burndown rates and overflow behaviour."
sources:
  - https://docs.claude.com/en/api/service-tiers
  - https://docs.claude.com/en/docs/build-with-claude/batch-processing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Service tiers and priority capacity

**Goal:** each workload runs on the capacity tier that matches its latency, availability and cost needs, and overflow behaviour is understood.

## The three Claude tiers
- **Standard:** the default for all API requests, best-effort availability.
- **Priority Tier:** requests are prioritised over all others to minimise "server overloaded" errors even at peak. Service tiers are labelled legacy: Priority Tier commitments are no longer available for purchase; organisations with an existing commitment can use it until the contract end date, and others needing guaranteed capacity are pointed to sales.
- **Batch:** for asynchronous workflows that can wait or benefit from being outside normal capacity (see the Message Batches API: all usage at 50 percent of standard prices, results within 24 hours or the batch expires).

| Workload | Tier |
|---|---|
| Interactive with an existing Priority Tier commitment | `service_tier: "auto"` |
| Interactive, normal | standard |
| Offline bulk (backfills, dataset labelling) | batch |

## The service_tier parameter
- `"auto"` (default): uses Priority Tier capacity if available, otherwise falls back to your other capacity.
- `"standard_only"`: uses only standard capacity, for when you do not want to spend Priority Tier capacity.
- The response `usage.service_tier` reports the tier that served the request (for example `"priority"`).
- With `auto` and a commitment on the model, `anthropic-priority-input-tokens-*` and `anthropic-priority-output-tokens-*` response headers (limit, remaining, reset) show your Priority Tier capacity; their presence indicates eligibility even if the request went over the limit.

## How requests are assigned and counted
A request goes to Priority Tier only when the organisation has enough Priority Tier capacity for both input and output tokens per minute; otherwise it proceeds at standard tier. Priority requests pull from both Priority Tier capacity and the regular rate limits, and are declined if they would exceed the rate limits.

Burndown against Priority Tier capacity: cache reads 0.1 tokens per token, cache writes 1.25 (5-minute TTL) or 2.00 (1-hour TTL), other input 1; US-only inference (`inference_geo: "us"`, Claude 4.6 and later) draws 1.1 per input or output token; other output 1.

## Commitments
A commitment is input tokens per minute, output tokens per minute, a duration (1, 3, 6 or 12 months) and a specific model version. Priority Tier targets 99.5 percent uptime, and traffic beyond committed capacity falls back to standard automatically. Priority Tier is supported on all available Claude models except Claude Fable 5.1, Claude Haiku 5.5, Claude Mythos 5.1, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5 and Claude Sonnet 5 (as of the page read); check the models overview.

## Operating practice (author's guidance, not from the sources)
- Measure peak tokens per minute, input and output separately, per model before sizing any commitment; review utilisation regularly.
- Keep tier selection in config per route so traffic can shift during incidents.
- Handle overload errors with retries and backoff, and fall back to another model or platform on critical paths.

## Verify
- [ ] Each route has a documented tier and fallback.
- [ ] `usage.service_tier` logged and dashboarded.
- [ ] Batch-eligible workloads moved off real-time endpoints.

## Checked

Confirmed against the Claude Service tiers page (read in full, apart from the code listings) and the Message Batches guide. Removed the OpenAI flex/priority, Amazon Bedrock, Vertex AI and Azure sections and their sources because those pages were not readable, and the claim that Priority Tier is a purchasable product (the page says it is legacy and no longer sold).

Method: docs-checked 2026-11-09 against https://docs.claude.com/en/api/service-tiers (served from platform.claude.com) and https://docs.claude.com/en/docs/build-with-claude/batch-processing
