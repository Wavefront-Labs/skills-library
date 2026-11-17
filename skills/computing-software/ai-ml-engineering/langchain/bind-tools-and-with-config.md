---
id: computing-software.ai-ml-engineering.langchain.bind-tools-and-with-config
name: bind-tools-and-with-config
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, runnable-bind, bind-tools, with-config, tool-choice, runnables, chat-models]
level: practitioner
status: verified
description: "Attach default arguments to runnables: bind_tools with tool_choice and strict, .bind for stop/kwargs, with_config for tags/run_name/recursion_limit, and when bindings are lost."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# bind, bind_tools and with_config

## bind_tools
```python
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Current weather for a city."""
    ...

llm = init_chat_model("anthropic:<model-id>")
llm_tools = llm.bind_tools([get_weather], tool_choice="auto")   # "any" / tool name to force
msg = llm_tools.invoke("Weather in Lisbon?")
msg.tool_calls        # [{'name': 'get_weather', 'args': {'city': 'Lisbon'}, 'id': ...}]
```
- `tool_choice`: `"auto"` (default), `"any"` (must call some tool) and a tool name (force that tool) work on `langchain-anthropic` and `langchain-openai` (checked by inspecting the bound kwargs). `"none"` is passed through by `langchain-openai` but `langchain-anthropic` treats it as a tool NAME (`{"type": "tool", "name": "none"}`), so do not use it there; just omit the tools.
- `strict=True` is added to each tool definition (`strict: True` in both the Anthropic and OpenAI payloads; OpenAI also sets `additionalProperties: false`).
- `parallel_tool_calls=False` forces at most one call per turn: OpenAI gets `parallel_tool_calls=False`, Anthropic gets `tool_choice={"type": "auto", "disable_parallel_tool_use": True}`.

## bind
Fixes invocation kwargs for every call: `llm.bind(stop=["\nObservation:"])`, `llm.bind(max_tokens=200)`. Bound kwargs merge with call-time kwargs.

## with_config
Runtime configuration rather than model arguments:
```python
chain = (prompt | llm_tools).with_config(run_name="weather_chain", tags=["prod", "v3"],
                                         metadata={"team": "assistants"}, max_concurrency=5)
```
Also `recursion_limit` for graphs and `configurable` values for configurable fields.

## Gotchas
- `bind_tools` returns a new runnable; calling `llm.invoke` still has no tools. Keep the bound object.
- Order matters with wrappers: `llm.bind_tools(...).with_retry()` keeps tools; `llm.with_retry().bind_tools(...)` fails because the retry wrapper has no `bind_tools` (run: `hasattr(llm.with_retry(), "bind_tools")` is False).
- Tool descriptions come from docstrings and type hints; poor docstrings cause wrong tool choice.

## Verify
- [ ] Inspect a trace to confirm the tools and tool_choice were sent in the request.
