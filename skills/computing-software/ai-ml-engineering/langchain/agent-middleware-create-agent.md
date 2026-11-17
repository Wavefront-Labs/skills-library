---
id: computing-software.ai-ml-engineering.langchain.agent-middleware-create-agent
name: agent-middleware-create-agent
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, agent-middleware, create-agent, langchain-v1, summarization-middleware, human-in-the-loop, dynamic-prompt]
level: practitioner
status: verified
description: "Customize LangChain v1 create_agent with middleware: built-ins (summarization, HITL, PII, call limits), before/after_model hooks and wrap_model_call."
sources:
  - https://docs.langchain.com/oss/python/langchain/middleware
  - https://docs.langchain.com/oss/python/langchain/agents
  - https://docs.langchain.com/oss/python/releases/langchain-v1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agent middleware in create_agent

**Context:** LangChain 1.x `create_agent` (built on LangGraph) runs the standard model -> tools loop. Middleware hooks into that loop instead of you rewriting the graph.

## Built-in middleware
```python
from langchain.agents import create_agent
from langchain.agents.middleware import (SummarizationMiddleware, HumanInTheLoopMiddleware,
                                         ModelCallLimitMiddleware, PIIMiddleware)
agent = create_agent(
    model="anthropic:<model-id>",
    tools=[search, send_email],
    system_prompt="You are a support agent.",
    middleware=[
        SummarizationMiddleware(model="anthropic:<small-model-id>", trigger=("tokens", 8000)),
        HumanInTheLoopMiddleware(interrupt_on={"send_email": True}),   # pause for approval
        ModelCallLimitMiddleware(run_limit=25),
        PIIMiddleware("email", strategy="redact"),
    ],
    checkpointer=checkpointer)                 # HITL needs a checkpointer to pause/resume
```
Other built-ins (langchain 1.4.6 exports) include `ToolCallLimitMiddleware`, `ModelFallbackMiddleware`, `ToolRetryMiddleware`, `ModelRetryMiddleware`, `ContextEditingMiddleware`, `LLMToolSelectorMiddleware`, `TodoListMiddleware`; check the docs for your installed version since the set grows.

## Custom hooks
```python
from langchain.agents.middleware import before_model, after_model, wrap_model_call, dynamic_prompt
from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

@before_model
def trim(state, runtime):
    if len(state["messages"]) > 40:
        # a plain slice does NOT trim: messages use the add_messages reducer (merge by id), so
        # the old messages stay (run: 8 in, 8 kept). Replace the whole list instead:
        return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *state["messages"][-40:]]}

@dynamic_prompt
def by_user(request):
    return f"You are helping {request.runtime.context.user_name}. Be concise."

@wrap_model_call
def route_model(request, handler):
    if len(request.messages) > 20:
        request = request.override(model=big_model)      # switch model for long conversations
    return handler(request)
```
- `before_model` / `after_model` (and `before_agent`/`after_agent`) read and update state.
- `wrap_model_call` / `wrap_tool_call` wrap the actual call: retries, caching, model routing, tool filtering per request.
- Order (docs, "Key rules"): `before_*` hooks run first to last, `after_*` hooks last to first, and `wrap_*` hooks nest with the first middleware wrapping all the others.
- `max_tokens_before_summary` still works but emits a DeprecationWarning; use `trigger=("tokens", n)` (langchain 1.4.6).
- `request.runtime.context` needs `context_schema=` on `create_agent` and `agent.invoke(..., context=Ctx(...))`.

## Gotchas
- Middleware runs on every loop iteration; keep it cheap.
- State updates must match the agent state schema; custom state keys need a `state_schema` on the middleware.

## Verify
- [ ] Trace shows hooks firing (e.g. summary messages, interrupts) on a scripted long conversation.
