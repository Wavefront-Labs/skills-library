---
id: computing-software.ai-ml-engineering.langchain.lcel-with-fallbacks-and-with-retry
name: lcel-with-fallbacks-and-with-retry
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, lcel, runnables, with-fallbacks, with-retry, provider-failover, llm-reliability]
level: practitioner
status: verified
description: "Make LCEL chains resilient: with_retry for transient errors, with_fallbacks to a second model or chain, ordering with SDK retries, and exception scoping."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LCEL: with_retry and with_fallbacks

**Goal:** a chain that survives rate limits, 5xx and provider outages without masking real bugs.

## Retry first, then fall back
```python
from anthropic import RateLimitError, APIStatusError, APIConnectionError
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

primary = ChatAnthropic(model="claude-sonnet-4-5", max_retries=0, timeout=60)   # SDK retries off: we own them
backup  = ChatOpenAI(model="gpt-4o-mini", max_retries=0, timeout=60)

primary_r = primary.with_retry(
    retry_if_exception_type=(RateLimitError, APIConnectionError),
    wait_exponential_jitter=True,
    stop_after_attempt=3,
)
llm = primary_r.with_fallbacks([backup], exceptions_to_handle=(RateLimitError, APIStatusError, APIConnectionError))
chain = prompt | llm | parser
```
- Every provider SDK already retries (the `anthropic` and `openai` SDKs default to `max_retries=2`, run; `ChatAnthropic.max_retries` reads 2, `ChatOpenAI.max_retries` reads `None` and defers to the SDK). Leaving that on and adding `with_retry` multiplies attempts (3 x 3 = 9) and delays the fallback by minutes. Pick one layer.
- `exceptions_to_handle` defaults to `(Exception,)` - a prompt bug (KeyError, ValidationError) then silently runs on the backup model (run). With `exceptions_to_handle=(RateLimitError,)` a `KeyError` propagated (run). Scope it to transport/provider errors.
- Fallback a whole sub-chain when prompts differ per provider: `(prompt_a | primary).with_fallbacks([prompt_b | backup])`. The fallback receives the **original input**, not the failed step's output (run).
- `exception_key="error"` passes the exception into the fallback's input dict (input must be a dict; a str input raised `ValueError`, run) - useful for "repair" fallbacks.

## Fallbacks for bad output, not just errors
Put the parser inside the fallback unit so a parse failure triggers the alternative:
```python
strict = (prompt | primary | PydanticOutputParser(pydantic_object=Answer))
chain = strict.with_fallbacks([prompt | stronger_model | PydanticOutputParser(pydantic_object=Answer)])
```

## Streaming caveat
Fallbacks only switch before the first chunk is emitted; a mid-stream failure surfaces as an error to the caller (run: a generator that yielded one chunk then raised propagated `RuntimeError`; one that failed before yielding fell back). Handle mid-stream failures at the app layer (retry the request, tell the user).

## Gotchas
- `with_retry` on a chain that has side effects (tool calls, DB writes) re-runs them; retry the model call, not the whole chain.
- Fallback models need compatible features: tool schemas, structured output, and parameters (model-specific limits on `temperature`, `max_tokens` and so on) - test the backup path explicitly.
- Log which branch served each request (callback or LangSmith metadata) or failover goes unnoticed for weeks.

## Verify
- [ ] Unit test forces the primary to raise `RateLimitError` (mock) and asserts the backup answered.
- [ ] A `ValueError` in your own code propagates instead of falling back.
- [ ] Total worst-case latency (attempts x timeout + backoff) is under the caller's timeout.
