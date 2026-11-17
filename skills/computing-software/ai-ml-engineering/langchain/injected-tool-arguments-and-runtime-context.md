---
id: computing-software.ai-ml-engineering.langchain.injected-tool-arguments-and-runtime-context
name: injected-tool-arguments-and-runtime-context
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, injectedtoolarg, tool-runtime, injected-state, runtime-context, tool-security]
level: practitioner
status: verified
description: "Hide arguments from the model with InjectedToolArg, InjectedState, InjectedStore and ToolRuntime so user ids, auth and graph state reach tools from server-side context."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://docs.langchain.com/oss/python/langchain/tools
  - https://langchain-ai.github.io/langgraph/how-tos/tool-calling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Injected tool arguments and runtime context

**Goal:** tools receive values the model must not choose (user id, tenant, DB handle, current graph state) without those values appearing in the tool schema sent to the LLM.

## Why
Anything in a tool's schema is model-controlled. If `get_orders(user_id)` exposes `user_id`, a prompt injection can ask for another user's orders. Injected arguments are stripped from the schema and filled by your code.

## InjectedToolArg (plain LangChain)
```python
from typing import Annotated
from langchain_core.tools import tool, InjectedToolArg

@tool
def get_orders(status: str, user_id: Annotated[str, InjectedToolArg]) -> list[dict]:
    """List the current user's orders with the given status."""
    return db.orders(user_id=user_id, status=status)

get_orders.tool_call_schema.model_json_schema()   # only 'status' (run; `get_input_schema()` still has both)
```
In a manual loop, merge the value in before executing: `get_orders.invoke({**tool_call["args"], "user_id": session.user_id})`.

## ToolRuntime (LangChain v1 agents)
```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

@dataclass
class Context:
    user_id: str

@tool
def get_orders(status: str, runtime: ToolRuntime[Context]) -> list[dict]:
    """List the current user's orders with the given status."""
    return db.orders(user_id=runtime.context.user_id, status=status)

agent = create_agent("anthropic:<model-id>", tools=[get_orders], context_schema=Context)
agent.invoke({"messages": [{"role": "user", "content": "open orders?"}]}, context=Context(user_id=auth.user_id))
```
`runtime` also exposes `state` (graph state), `store` (long-term memory), `stream_writer` (custom progress events) and `tool_call_id` (run; langchain 1.4.6 also lists `config`, `execution_info`, `server_info`, `tools`). It is not part of the tool schema sent to the model (run: only `status` appears).

## LangGraph annotations
With `ToolNode`: `Annotated[dict, InjectedState]` (whole state or `InjectedState("field")`), `Annotated[BaseStore, InjectedStore()]`, and `Annotated[str, InjectedToolCallId]` (needed to return a `Command` with a matching `ToolMessage`). A parameter typed `config: RunnableConfig` is injected automatically.

## Gotchas
- Tests that call `tool.invoke(args)` must pass injected values themselves; missing ones raise a pydantic `ValidationError` (run).
- Do not describe injected params in the docstring; the model may try to supply them.
- Injection is not authorisation: the tool still checks the user may access the resource.

## Verify
- [ ] The schema sent to the model (`tool_call_schema`) contains no identity or credential fields.
- [ ] A prompt asking for another user's data returns only the caller's data.
