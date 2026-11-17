---
id: computing-software.ai-ml-engineering.langchain.langgraph-stream-modes
name: langgraph-stream-modes
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langgraph, stream-mode, streaming, astream, token-streaming, custom-stream]
level: practitioner
status: verified
description: "Stream LangGraph runs with the right stream_mode: values, updates, messages (LLM tokens with metadata), custom via get_stream_writer, debug, multiple modes and subgraphs."
sources:
  - https://langchain-ai.github.io/langgraph/how-tos/streaming/
  - https://docs.langchain.com/oss/python/langgraph/streaming
  - https://langchain-ai.github.io/langgraph/concepts/streaming/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LangGraph stream modes

## Modes
| `stream_mode` | Yields | Use |
|---|---|---|
| `"values"` | full state after each step | debugging, simple UIs |
| `"updates"` | `{node_name: state_delta}` per step | progress indicators, logging |
| `"messages"` | `(message_chunk, metadata)` LLM tokens from any node | chat token streaming |
| `"custom"` | anything nodes write via the stream writer | tool progress, partial results |
| `"debug"` | detailed task/checkpoint events | deep debugging |
| `"checkpoints"`, `"tasks"` | checkpoint and task events | listed on the docs streaming page |

## Token streaming
```python
async for chunk, meta in graph.astream({"messages": [("user", q)]}, config, stream_mode="messages"):
    if meta["langgraph_node"] == "agent" and chunk.content:
        print(chunk.content, end="", flush=True)
```
`meta` includes `langgraph_node`, tags and the model run info; internal LLM calls (e.g. a router) are streamed too (run: a tagged model's tokens arrived with `meta["tags"] == ["internal"]`), so filter by node name or tag those models (`llm.with_config(tags=["internal"])`) and skip that tag.

## Custom events
```python
from langgraph.config import get_stream_writer
def fetch_docs(state):
    writer = get_stream_writer()
    for i, url in enumerate(state["urls"]):
        writer({"progress": f"fetched {i + 1}/{len(state['urls'])}"})
    return {...}
for mode, data in graph.stream(inputs, stream_mode=["updates", "custom"]):
    print(mode, data)
```
Multiple modes yield `(mode, data)` tuples.

## Subgraphs
`graph.stream(inputs, stream_mode="updates", subgraphs=True)` yields `(namespace, data)` so you can see inner-graph progress (run: namespace `("research:<task-id>",)` for the inner node, `()` for the parent).

## Serving
Expose over SSE/WebSocket from FastAPI by iterating `astream` and serializing chunks; LangGraph Platform provides streaming endpoints with the same modes.

## Gotchas
- Python < 3.11 async (docs warning): pass `RunnableConfig` explicitly to `ainvoke()` for `messages` mode, and `get_stream_writer` does not work in async nodes there; add a `writer` parameter to the node instead.
- `"values"` re-sends the whole state each step; heavy for big states.

## Verify
- [ ] A UI receives first token within expected latency; internal router tokens are not shown.
