---
id: computing-software.ai-ml-engineering.llm-application-engineering.batch-api-for-offline-llm-workloads
name: batch-api-for-offline-llm-workloads
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, prompt-caching, batch-api, message-batches, offline-inference, llm-cost, evaluation-runs]
level: practitioner
status: docs-checked
description: "Run large offline LLM jobs on the Claude Message Batches API: custom_id mapping, polling, partial failures, retries and when batch is wrong."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/batch-processing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch APIs for offline LLM workloads

**Goal:** process thousands to millions of non-urgent requests (classification backfills, eval runs, document enrichment) at a large discount, without managing rate limits yourself.

## Claude Message Batches
```python
reqs = [{"custom_id": f"doc-{d.id}",
         "params": {"model": MODEL, "max_tokens": 1024,
                    "messages": [{"role": "user", "content": build_prompt(d)}]}} for d in docs]
batch = client.messages.batches.create(requests=reqs)
while client.messages.batches.retrieve(batch.id).processing_status != "ended":
    time.sleep(60)
for r in client.messages.batches.results(batch.id):
    if r.result.type == "succeeded":
        save(r.custom_id, r.result.message.content)
    else:                                  # errored / canceled / expired
        retry_queue.append(r.custom_id)
```
- Discount: all usage is charged at 50 percent of standard API prices (the discount stacks with prompt caching, but cache hits are best-effort because requests run concurrently).
- Most batches finish within 1 hour; a batch expires if processing does not complete within 24 hours, and requests not sent to the model by then are `expired` and not billed. Results stay downloadable for 29 days.
- Results come back in **any order** - always key by `custom_id` (1 to 64 characters: letters, digits, hyphens, underscores).
- Each request carries standard Messages API parameters in `params`. Vision, tool use, system messages, multi-turn conversations and extended thinking are supported; `stream: true` and `max_tokens: 0` are not.
- Validation of `params` happens asynchronously and errors appear only when the batch ends, so test the request shape against the Messages API first.
- The result types are `succeeded`, `errored`, `canceled` and `expired`; only `succeeded` requests are billed. An `errored` result with an `invalid_request_error` needs its request fixed before resending; other errors can be retried directly.

## Operating it
- A batch is limited to 100,000 requests or 256 MB, whichever comes first; chunk large jobs into several batches so a problem in one doesn't stall all.
- Make work idempotent: a results table keyed by `custom_id`; re-submit only missing/failed IDs.
- Validate a small sample synchronously first - a prompt bug discovered after 200k requests is expensive even at half price.
- Store the prompt version and model with results.

## When not to use batch
Anything a user waits for; workloads that need iterative multi-turn tool use with your own tools between turns (each batch item is one request); jobs needing results in minutes.

## Verify
- [ ] Pilot of ~100 requests checked before the full submission.
- [ ] All results joined by `custom_id`; failures retried.
- [ ] Cost per item compared with synchronous baseline.

## Checked

Confirmed against the Claude Message Batches (batch processing) guide, read in part (limitations, supported features and unsupported parameters, pricing statement, request shape, polling, result types, ordering and prompt caching sections; the long multi-language code listings were not read line by line). Removed the OpenAI Batch section and source (page not readable), the claim that structured outputs are supported, and the unconfirmed "typically well within the window" wording; added the documented limits.

Method: docs-checked 2026-11-09 against https://docs.claude.com/en/docs/build-with-claude/batch-processing (served from platform.claude.com)
