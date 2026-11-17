---
id: computing-software.ai-ml-engineering.langchain.batch-and-abatch-max-concurrency
name: batch-and-abatch-max-concurrency
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, lcel, langchain-batch, max-concurrency, abatch, batch-as-completed, throughput]
level: practitioner
status: verified
description: "Run LCEL chains over many inputs with batch, abatch and batch_as_completed: max_concurrency, return_exceptions, rate-limit interplay and when to use provider batch APIs instead."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# batch / abatch with max_concurrency

**Goal:** process hundreds to thousands of inputs through a chain quickly without tripping provider rate limits or losing the whole run to one failure.

## Basics
```python
results = chain.batch(inputs, config={"max_concurrency": 8}, return_exceptions=True)
for inp, r in zip(inputs, results):
    if isinstance(r, Exception):
        failed.append((inp, r))
```
- Order of `results` matches `inputs` (run). `batch_as_completed` yields `(index, result)` pairs in completion order, not input order (run).
- Sync `batch` uses a thread pool; `abatch` uses asyncio with a semaphore. Both honour `max_concurrency` (config key `max_concurrency`; default is no explicit cap).
- Without `return_exceptions=True` the first exception aborts and you lose completed results.
- Per-input configs: pass a list of configs the same length as inputs (a shorter list raises `ValueError`, run) (e.g., distinct `run_name` or metadata per item).

## Stream results as they finish
```python
for idx, out in chain.batch_as_completed(inputs, config={"max_concurrency": 8}, return_exceptions=True):
    save(inputs[idx]["id"], out)          # checkpoint progress; resume skips saved ids
```
`abatch_as_completed` is the async twin. Checkpointing per item makes a 10k-item job restartable.

## Sizing concurrency
Concurrency x average tokens per request / latency must fit under your tokens-per-minute limit. Start at 4-8, watch for 429s, raise gradually. Combine with an `InMemoryRateLimiter` on the model for a hard request-rate ceiling, and keep SDK `max_retries` for 429s.

## When not to use batch()
For non-urgent jobs of thousands of requests, provider batch APIs (Claude Message Batches, OpenAI Batch) are 50% cheaper and handle rate limiting server-side; build the prompts with the same LCEL prompt template (`prompt.invoke(x).to_messages()`) and submit them there.

## Gotchas
- `batch` on a chat model directly takes a list of message lists/strings, not dicts.
- Very large input lists held in memory with results: chunk into pages of ~1k.
- Errors returned as values are easy to forget - count them and fail the job above a threshold.

## Verify
- [ ] Run of N items reports success/failure counts and retries only the failures.
- [ ] No sustained 429s at chosen `max_concurrency` (check provider rate-limit headers or logs).
