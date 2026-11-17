---
id: computing-software.ai-ml-engineering.llm-application-engineering.llm-rate-limits-retries-and-backoff
name: llm-rate-limits-retries-and-backoff
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, rate-limits, exponential-backoff, retry-after, http-429, concurrency-control, llm-reliability]
level: practitioner
status: docs-checked
description: "Handle LLM API rate limits and transient errors: RPM and token limits, retry-after, exponential backoff with jitter, client-side throttling and overload handling."
sources:
  - https://docs.claude.com/en/api/rate-limits
  - https://docs.claude.com/en/api/errors
  - https://platform.openai.com/docs/guides/rate-limits
  - https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limits, retries and backoff for LLM APIs

**Goal:** high throughput without 429 storms, and graceful behaviour when the provider is overloaded.

## Know the limits
Providers limit **requests per minute** and **tokens per minute** (often input and output separately), per model and per organisation tier. Response headers report remaining capacity and reset times (Claude: `anthropic-ratelimit-*` headers). A 429 from exceeding a limit can carry `retry-after` (seconds to wait); not every 429 does, and a monthly spend-cap 429 never does and keeps failing until access resumes. A 529 `overloaded_error` means the API is temporarily overloaded across all users, distinct from your quota. Sharp traffic increases can trigger acceleration-limit 429s, so ramp up gradually.

## Retries
- Anthropic's official SDK retries transient failures (connection errors, rate limits, 5xx) with exponential backoff, twice by default, honouring `retry-after`; configure it with `max_retries` rather than reimplementing.
- Custom logic: exponential backoff with jitter, follow `retry-after` when present, limit both attempts and total retry time. If you retry in your app, disable or account for SDK retries so loops do not multiply.
- Don't retry errors that need action (quota, billing, invalid requests).

## Throttle on the client
Retries are a last resort; avoid hitting limits:
```python
sem = asyncio.Semaphore(32)                       # concurrency cap
async def call(msgs):
    async with sem:
        return await aclient.messages.create(model=MODEL, max_tokens=1024, messages=msgs)
```
For token-based limits, a token bucket keyed on estimated input + max output tokens per request smooths load. Distributed workers need a shared limiter (Redis) or per-worker quotas.

## Offload and degrade
- Non-urgent work -> offline or queued processing.
- Under sustained overload: fall back to another model/provider, shed low-priority traffic, or queue with user-visible status.
- Ask the provider about higher limits ahead of launches.

## Idempotency
Retried requests may produce different outputs and double side effects downstream (tool actions, emails). Make side-effecting steps idempotent by key, and log retries.

## Checked
2026-11-01. Confirmed against Anthropic's rate limits and errors pages (token bucket, RPM/ITPM/OTPM, `anthropic-ratelimit-*` headers, `retry-after`, spend-cap 429 without it, 529, acceleration limits, SDK retry behaviour and `max_retries`) and OpenAI's rate limits guide (Retry-After then exponential backoff with jitter, limit attempts and total time, avoid nested retry loops, do not retry errors needing action). Removed: 408/409 list, timeout figure, OpenAI header names, batch discount, error-rate threshold.
Method: documentation only; no commands were run.

## Verify
- [ ] Load test at target throughput shows few or no 429s after throttling.
- [ ] Retry policy honours `retry-after`; jitter present.
- [ ] Fallback/shedding behaviour tested with an injected 429/529 storm.
