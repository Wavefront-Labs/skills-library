---
id: computing-software.ai-ml-engineering.langchain.langgraph-subgraphs-and-send-map-reduce
name: langgraph-subgraphs-and-send-map-reduce
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langgraph, stategraph, subgraphs, send-api, map-reduce, parallel-branches]
level: practitioner
status: verified
description: "Compose LangGraph workflows from subgraphs (shared or transformed state) and fan out dynamic parallel work with the Send API for map-reduce patterns."
sources:
  - https://langchain-ai.github.io/langgraph/how-tos/subgraph/
  - https://langchain-ai.github.io/langgraph/how-tos/graph-api/#map-reduce-and-the-send-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subgraphs and Send map-reduce

## Subgraph sharing state keys - add it as a node
```python
sub = sub_builder.compile()               # no checkpointer: inherits the parent's
parent.add_node("research", sub)          # parent and sub share e.g. "messages"
```

## Subgraph with a different schema - call it from a node
```python
def run_research(state: Parent) -> dict:
    out = sub.invoke({"topic": state["question"]})
    return {"notes": out["summary"]}
parent.add_node("research", run_research)
```
Mapping in and out explicitly keeps internal keys private and lets teams version subgraphs independently.

Persistence: compile subgraphs **without** a checkpointer (parent's propagates, interrupts inside subgraphs work). `checkpointer=True` gives a subgraph its own memory across calls (e.g., a stateful specialist agent). Stream nested output with `app.stream(inp, cfg, subgraphs=True)`; inspect with `app.get_state(cfg, subgraphs=True)`.

## Send: dynamic fan-out
```python
from langgraph.types import Send
class State(TypedDict):
    docs: list[str]
    summaries: Annotated[list[str], operator.add]   # reducer collects branch results

def fan_out(state: State):
    return [Send("summarize", {"doc": d}) for d in state["docs"]]

def summarize(item: dict) -> dict:                    # receives the Send payload, not full state
    return {"summaries": [chain.invoke(item["doc"])]}

g.add_conditional_edges("split", fan_out, ["summarize"])
g.add_edge("summarize", "combine")                    # runs after all branches finish
```
- Branches run in the same superstep, in parallel (run: 3 docs gave `["A", "B", "C"]`); the reducer merges results (order not guaranteed - include an index if order matters).
- Limit fan-out width with `max_concurrency` in config to respect rate limits.
- One failing branch fails the superstep; catch errors inside the branch and return an error marker if partial results are acceptable.

## Verify
- [ ] Fan-out of N docs produces N summaries (count assertion).
- [ ] Interrupt inside a subgraph resumes correctly with the parent's checkpointer.
