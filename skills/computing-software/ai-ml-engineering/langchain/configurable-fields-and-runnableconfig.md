---
id: computing-software.ai-ml-engineering.langchain.configurable-fields-and-runnableconfig
name: configurable-fields-and-runnableconfig
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, lcel, runnables, configurable-fields, configurable-alternatives, runnableconfig, runtime-configuration]
level: practitioner
status: verified
description: "Change models and parameters at runtime in LCEL with configurable_fields / configurable_alternatives, and pass tags, metadata, callbacks and limits through RunnableConfig."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# configurable_fields, configurable_alternatives and RunnableConfig

**Goal:** one chain object, many runtime variants (model, prompt, max_tokens) selected per request, with tracing metadata flowing through every step.

## configurable_fields - tweak a parameter
```python
from langchain_core.runnables import ConfigurableField
llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=512).configurable_fields(
    max_tokens=ConfigurableField(id="llm_max_tokens", name="Max tokens"),
)
chain = prompt | llm
chain.invoke({"q": "..."}, config={"configurable": {"llm_max_tokens": 2048}})
```

## configurable_alternatives - swap a whole component
```python
llm = ChatAnthropic(model="claude-sonnet-4-5").configurable_alternatives(
    ConfigurableField(id="llm"), default_key="sonnet",
    opus=ChatAnthropic(model="claude-opus-4-1"),
    openai=ChatOpenAI(model="gpt-4o"),
)
chain.with_config(configurable={"llm": "opus"}).invoke(inp)
```
Works for prompts too (A/B two prompt templates under one id). `chain.config_schema().model_json_schema()` lists every configurable id - LangServe/LangGraph Platform expose it to clients, so do not make security-relevant things (API keys, base URLs) configurable from untrusted input.

## RunnableConfig keys
`tags`, `metadata`, `callbacks`, `run_name`, `run_id`, `max_concurrency`, `recursion_limit`, `configurable`.
```python
chain.invoke(inp, config={"tags": ["checkout"], "metadata": {"tenant": t_id, "prompt_v": "7"},
                          "run_name": "answer-question", "max_concurrency": 4})
```
Tags/metadata propagate to child runs (visible in LangSmith and callbacks).

## Reading config inside your own step
```python
from langchain_core.runnables import RunnableConfig, RunnableLambda
def lookup(x: dict, config: RunnableConfig) -> dict:
    tenant = config["metadata"]["tenant"]
    return {**x, "docs": search(x["q"], tenant)}
chain = RunnableLambda(lookup) | prompt | llm
```
In async code, accept `config` and pass it explicitly to nested `ainvoke(..., config=config)` calls (langchain-core source comments call this required on older Python; passing it is safe on every version), or child runs can detach from the trace. Tags and metadata do reach child steps (run: a second `RunnableLambda` saw `tags=["checkout"]`, `metadata={"tenant": "t"}`).

## Gotchas
- Unknown keys in `configurable` are ignored silently - a typo means the default runs (run: `llm_max_tokes` left `max_tokens` at 512). An unknown alternative VALUE raises `ValueError: Unknown alternative`. Assert on `config_schema()` in tests.
- `configurable` values are per-invocation; `with_config` returns a new runnable (immutable), it does not mutate the original.
- LangGraph uses `configurable["thread_id"]`; keep your own ids namespaced to avoid collisions.

## Verify
- [ ] Each alternative key invoked once in a test; trace shows the expected model name.
- [ ] Metadata such as tenant appears on child runs in LangSmith.
