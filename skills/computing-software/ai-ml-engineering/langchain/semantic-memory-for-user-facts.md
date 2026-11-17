---
id: computing-software.ai-ml-engineering.langchain.semantic-memory-for-user-facts
name: semantic-memory-for-user-facts
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langgraph, memory, semantic-memory, long-term-memory, langmem, memory-tools, personalization]
level: practitioner
status: docs-checked
description: "Give an agent LangMem memory tools (create_manage_memory_tool, create_search_memory_tool) over a LangGraph store, with per-user and shared team namespaces."
sources:
  - https://langchain-ai.github.io/langmem/guides/memory_tools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semantic memory for user facts with LangMem memory tools

**Goal:** the assistant stores and searches facts and preferences across sessions. LangMem provides tools that let an agent store and search memories in a LangGraph store.

## Hot-path memory tools
```python
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool

store = InMemoryStore(index={"dims": 1536, "embed": "openai:text-embedding-3-small"})

agent = create_react_agent(
    "anthropic:claude-3-5-sonnet-latest",
    tools=[
        create_manage_memory_tool(namespace=("memories", "{user_id}")),
        create_search_memory_tool(namespace=("memories", "{user_id}")),
    ],
    store=store,
)
agent.invoke(
    {"messages": [{"role": "user", "content": "Remember my favorite color is blue"}]},
    config={"configurable": {"user_id": "user-a"}},     # fills {user_id}: namespace ("memories", "user-a")
)
```
- `InMemoryStore` works for development but does not persist between restarts; for production use a persistent store such as `AsyncPostgresStore`.
- The `{user_id}` placeholder is filled from the run config, and both tools share the same namespace for consistency.
- The same `("memories", "{user_id}")` structure can express personal, team (for example `("memories", "team-product")`) or project namespaces.

## Shared storage between agents
The store is shared within a deployment, so agents on a team can write to agent-specific namespaces and read from a shared team namespace:
```python
# agent A
tools = [create_manage_memory_tool(namespace=("memories", "team_a", "agent_a")),
         create_search_memory_tool(namespace=("memories", "team_a"))]
```
A second agent writes to `("memories", "team_a", "agent_b")` and also searches `("memories", "team_a")`.

## Checked
Method: docs-checked 2026-11-09 against the LangMem "How to Use Memory Tools" guide (read basic usage and shared storage sections, lines 1501-1640 of the saved page). Dropped the background memory manager, retrieval, consolidation, privacy and evaluation sections, and the LangMem home and LangGraph memory-concepts sources, which were not read.
