---
id: computing-software.ai-ml-engineering.langchain.langgraph-state-reducers-and-conditional-edges
name: langgraph-state-reducers-and-conditional-edges
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langgraph, stategraph, state-reducers, conditional-edges, add-messages, command, graph-routing]
level: practitioner
status: verified
description: "Design LangGraph state with TypedDict and reducers (add_messages, operator.add), route with conditional edges or Command, and avoid concurrent-update and recursion errors."
sources:
  - https://langchain-ai.github.io/langgraph/concepts/low_level/
  - https://langchain-ai.github.io/langgraph/how-tos/graph-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LangGraph state, reducers and conditional edges

## State schema with reducers
```python
from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]     # append / update-by-id / RemoveMessage
    findings: Annotated[list[str], operator.add] # concatenate from parallel branches
    attempts: int                                # no reducer: last write wins
```
Nodes return **partial updates** (`{"attempts": s["attempts"] + 1}`), never the whole state. Without a reducer, two nodes writing the same key in the same superstep raise `InvalidUpdateError` (run: "Can receive only one value per step") - add a reducer for anything written by parallel branches.

Use separate `input_schema` / `output_schema` (StateGraph kwargs) to hide internal keys from callers.

## Conditional edges
```python
def route(state: State) -> str:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return "done" if state["attempts"] < 3 else "give_up"

g = StateGraph(State)
g.add_node("agent", agent); g.add_node("tools", tools); g.add_node("give_up", give_up)
g.add_edge(START, "agent")
g.add_conditional_edges("agent", route, {"tools": "tools", "done": END, "give_up": "give_up"})
g.add_edge("tools", "agent")
app = g.compile()
```
The path map documents possible targets for visualisation (`app.get_graph().draw_mermaid()`) and catches typos at compile time (run: unknown target raised `ValueError` at `compile()`).

## Command: update and route from inside a node
```python
from langgraph.types import Command
from typing import Literal
def review(state: State) -> Command[Literal["agent", "__end__"]]:
    ok = check(state)
    return Command(update={"attempts": state["attempts"] + 1}, goto=END if ok else "agent")
```
Type the return so the graph knows edges. Prefer conditional edges when routing depends only on state; use Command when the node computes both the update and the route.

## Loops and limits
Each superstep counts toward `recursion_limit`. The default was 25 in older LangGraph, but langgraph 1.2.16 sets `DEFAULT_RECURSION_LIMIT` to 10007 (env `LANGGRAPH_DEFAULT_RECURSION_LIMIT`; read from source), so set it explicitly: `app.invoke(inp, {"recursion_limit": 50})`. Hitting it raises `GraphRecursionError` (run, limit 10) - keep an explicit counter in state and route to a graceful exit before the hard limit.

## Verify
- [ ] Mermaid diagram matches the intended flow.
- [ ] Test with parallel branches writing the same key passes (reducer present).
- [ ] Loop exits via the counter path, not GraphRecursionError, in a forced-failure test.
