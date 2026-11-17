---
id: computing-software.ai-ml-engineering.langchain.rate-limiting-and-caching-llm-calls
name: rate-limiting-and-caching-llm-calls
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, inmemoryratelimiter, llm-cache, rate-limits, sqlitecache, set-llm-cache, cost-control]
level: practitioner
status: verified
description: "Throttle LangChain chat model requests with InMemoryRateLimiter and cut repeat cost with LLM caches (in-memory, SQLite, Redis), including cache-key and multi-process caveats."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limiting and caching LLM calls

## Client-side rate limiter
```python
from langchain_core.rate_limiters import InMemoryRateLimiter
limiter = InMemoryRateLimiter(requests_per_second=2, check_every_n_seconds=0.1, max_bucket_size=10)   # defaults: 1 rps, 0.1 s, bucket 1; run: 6 calls at 5 rps, bucket 1 took 1.2 s
llm = ChatAnthropic(model="claude-haiku-4-5", rate_limiter=limiter)
```
- Token bucket on **requests**, not tokens - large prompts can still hit tokens-per-minute limits; keep SDK retries for 429.
- Thread-safe within one process only. Ten workers each with 2 rps = 20 rps. For fleets, divide the budget per worker or use a shared limiter (Redis) / an LLM gateway.
- Share one limiter instance across all models that draw from the same provider quota.

## LLM response cache
```python
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache        # or InMemoryCache, RedisCache, RedisSemanticCache
set_llm_cache(SQLiteCache(database_path=".langchain.db"))
llm = ChatAnthropic(model="claude-haiku-4-5")              # cache=False on a model opts out; cache=<obj> overrides (run: both behaved as described)
```
- Key = serialized prompt + model params string. Any change (model, max_tokens, tool list) is a miss.
- Exact-match caches suit deterministic jobs: eval reruns, notebooks, CI tests (record once, replay offline), backfills.
- Semantic caches return answers for *similar* prompts - risky for user-specific or fact-sensitive answers; scope keys by tenant and set a similarity threshold you validated.
- Cached responses do not refresh; add TTL (Redis `ttl=`) when underlying data changes.

## Distinguish from provider prompt caching
LLM cache skips the call entirely; provider prompt caching (Claude `cache_control`, OpenAI automatic) still calls the model but reuses the processed prefix. Use both: prompt caching for long shared prefixes, LLM cache for identical full requests.

## Gotchas
- Global `set_llm_cache` affects every model in the process - surprising in tests; reset with `set_llm_cache(None)` (run: `get_llm_cache()` then returns `None`). `RedisCache(redis_, *, ttl=None)` takes the TTL.
- Streaming and the cache (run, langchain-core 1.6.12, `InMemoryCache`): `stream()` did not read the cache (the model's `_stream` ran again on a second identical `stream()`), but a later `invoke()` of the same prompt was served from the entry the first stream wrote. Do not rely on `stream()` for cache hits.
- Never cache responses containing other users' data under a key that omits user/tenant.

## Verify
- [ ] Second identical call returns in milliseconds with no provider request (check usage logs).
- [ ] Load test at expected concurrency shows no sustained 429s with the limiter configured.
