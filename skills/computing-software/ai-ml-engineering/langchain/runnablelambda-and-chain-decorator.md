---
id: computing-software.ai-ml-engineering.langchain.runnablelambda-and-chain-decorator
name: runnablelambda-and-chain-decorator
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, runnablelambda, lcel, chain-decorator, custom-runnables, runnables]
level: practitioner
status: verified
description: "Turn plain Python into LCEL runnables with RunnableLambda and @chain: sync/async pairs, config propagation for tracing, streaming generators and when to avoid lambdas."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RunnableLambda and @chain

**Use when:** you need custom logic (formatting, validation, lookups) inside an LCEL pipeline and still want `.invoke/.batch/.stream`, tracing and config passing.

## Wrapping functions
```python
from langchain_core.runnables import RunnableLambda, chain, RunnableConfig

def to_upper(text: str) -> str:
    return text.upper()

async def ato_upper(text: str) -> str:
    return text.upper()

upper = RunnableLambda(to_upper, afunc=ato_upper)      # provide async twin to avoid thread offloading
pipeline = prompt | model | StrOutputParser() | upper
```
Any function placed in a `|` chain is auto-wrapped as RunnableLambda, but explicit wrapping lets you name it (`.with_config(run_name="upper")`) for traces.

## Multiple inputs
Runnables take one input; pass a dict and unpack inside:
```python
def join(d: dict) -> str:
    return f"{d['question']}\n\nContext:\n{d['context']}"
```

## @chain for composite logic
```python
@chain
def answer(question: str, config: RunnableConfig) -> str:
    docs = retriever.invoke(question, config=config)          # pass config so child runs nest in the trace
    ctx = "\n\n".join(d.page_content for d in docs)
    return (prompt | model | StrOutputParser()).invoke({"question": question, "context": ctx}, config=config)
```
Accepting a `config` parameter gives access to callbacks, tags and `configurable` values; forwarding it keeps tracing and cancellation intact.

## Streaming
A RunnableLambda processes the whole input; to stream through a custom step, write a generator that consumes an iterator (run: a fake model streamed through it yielded `H`, `E`, `L`, ...):
```python
def uppercase_stream(chunks):
    for c in chunks:
        yield c.upper()
streaming_chain = prompt | model | StrOutputParser() | uppercase_stream
```

## Gotchas
- Lambdas returning a Runnable are invoked recursively (run) (useful for routing, surprising otherwise).
- Exceptions inside propagate; combine with `.with_retry()` / `.with_fallbacks()` on the lambda when calling flaky services.
- For multi-step control flow with state, loops or retries across steps, LangGraph is clearer than nested lambdas.

## Verify
- [ ] LangSmith (or `astream_events`) trace shows the custom step with its name and nested child runs.
