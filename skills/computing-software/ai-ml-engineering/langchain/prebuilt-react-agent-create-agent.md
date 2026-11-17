---
id: computing-software.ai-ml-engineering.langchain.prebuilt-react-agent-create-agent
name: prebuilt-react-agent-create-agent
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph, agents, create-agent, tool-calling, structured-response, checkpointer]
level: practitioner
status: docs-checked
description: "Build a tool-calling agent with LangChain's create_agent: model strings, tools, system_prompt, response_format, thread_id memory via a checkpointer, state_schema."
sources:
  - https://docs.langchain.com/oss/python/langchain/agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prebuilt agent: create_agent

**Goal:** a working tool-calling agent in a few lines, with memory, before deciding whether you need a custom graph. `create_agent` is the current LangChain agent harness: a model calling tools in a loop until the task is complete, shaped by the prompt, tools and middleware.

## Build
```python
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(
    model="anthropic:claude-sonnet-5",     # "provider:model" string or an initialized model instance
    tools=[search],                        # any Python callable, LangChain tool or tool dict
    system_prompt="You are a helpful assistant. Be concise and accurate.",
    checkpointer=InMemorySaver(),          # conversation memory per thread
)
```
- `system_prompt` accepts a string or a `SystemMessage`; use middleware for prompts that change at runtime.
- Extend the harness with middleware for more advanced capabilities.

## Invoke with memory
```python
from langchain_core.utils.uuid import uuid7
config = {"configurable": {"thread_id": str(uuid7())}}
result = agent.invoke({"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}, config=config)
result = agent.invoke({"messages": [{"role": "user", "content": "What about tomorrow?"}]}, config=config)   # same thread_id keeps history
```
Persisting history with `thread_id` requires a checkpointer. When deployed on LangSmith one is provisioned automatically; locally pass one explicitly.

## Structured final answer
```python
from pydantic import BaseModel
class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="anthropic:claude-sonnet-5", tools=tools, response_format=Answer)
agent.invoke({"messages": [...]})["structured_response"]     # Answer(...)
```
Strategies are covered in the Structured output page.

## Agent state
State is `AgentState`, which has an append-only `messages` list. Add custom fields by subclassing it and passing `state_schema=MyState` to `create_agent`; middleware hooks (`before_model`, `after_model`) receive the state and can return updates to merge.

## Verify
- [ ] The agent answers tool-requiring questions via tools (inspect `messages` for tool messages).
- [ ] Memory persists across turns on the same `thread_id` and not across threads.

## Checked
Method: docs-checked 2026-11-09 against https://docs.langchain.com/oss/python/langchain/agents (model, tools, system prompt, structured output, state, invoke sections read; examples grepped). Dropped the older langgraph create_react_agent code, recursion_limit, GraphRecursionError and streaming claims because the page read does not cover them, plus the two unread langgraph.github.io sources.
