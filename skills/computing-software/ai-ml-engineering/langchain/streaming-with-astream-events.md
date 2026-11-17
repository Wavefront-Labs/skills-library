---
id: computing-software.ai-ml-engineering.langchain.streaming-with-astream-events
name: streaming-with-astream-events
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, lcel, langchain-streaming, astream-events, astream, token-streaming, runnables]
level: practitioner
status: docs-checked
description: "Stream tokens and intermediate steps from LCEL with stream/astream and astream_events v2: event table, filtering, and why some chain steps break streaming."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/streaming.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/concepts/streaming.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming with astream and astream_events

**Goal:** show tokens as they are generated and surface progress from inner steps (retrieval, tools) to a UI.

## The APIs
1. `stream` (sync) and `astream` (async): stream outputs from a single Runnable (such as a chat model) or any LangGraph workflow.
2. `astream_events` (async only): access custom events and intermediate outputs from applications built entirely with LCEL. The concepts page notes it is available but not needed with LangGraph.
3. `astream_log`: legacy async API, not recommended for new projects.

If streaming does not appear in real time, check that async code uses the async methods (`ainvoke`, `astream`).

## Output streaming
```python
async for chunk in chain.astream({"q": q}):
    print(chunk, end="", flush=True)   # str chunks when the chain ends in StrOutputParser
```
Streaming is only possible if every step can process an input stream, handling one chunk at a time and yielding an output chunk. Models and parsers such as `StrOutputParser` and `JsonOutputParser` do (the JSON parser yields growing partial objects like `{'countries': [{'name': 'France'}]}`).

Any step that operates on a finalised input rather than a stream breaks streaming from `stream`/`astream`. Fix it with a generator function that consumes the input stream:
```python
async def extract_names(chunks):          # async generator over the parser's partial output
    async for text in chunks:
        ...
        yield name
chain = model | JsonOutputParser() | extract_names
```
Custom functions can be designed to return generators so they can operate on streams.

## Event streaming
```python
async for ev in chain.astream_events({"q": q}, version="v2"):
    if ev["event"] == "on_chat_model_stream":
        token = ev["data"]["chunk"].content      # AIMessageChunk
```
- The guide demonstrates the v2 API, which needs `langchain-core >= 0.2`. For `langchain-core < 0.3.37` set `version="v2"` explicitly.
- Events documented in the table: `on_chat_model_start|stream|end`, `on_llm_start|stream|end`, `on_chain_start|stream|end`, `on_tool_start|end`, `on_retriever_start|end`, `on_prompt_start|end`, and parser events such as `on_parser_stream`. Event fields include `event`, `name`, `run_id`, `tags`, `metadata`, `data`, `parent_ids`.
- Name steps with `.with_config({"run_name": "model"})` or tag them with `.with_config({"tags": ["my_chain"]})`, then filter with `include_names=[...]`, `include_types=["chat_model"]` or `include_tags=[...]`.
- `astream_events` still yields events from intermediate steps that support streaming even when a downstream step breaks final-output streaming.
- Custom data can be surfaced through `astream_events` with `dispatch_custom_event` / `adispatch_custom_event` (see the custom callback events how-to).
- If you invoke runnables inside your own tools, propagate callbacks to them or no stream events are generated. `RunnableLambda` and the `@chain` decorator propagate callbacks automatically.

## Verify
- [ ] Time to first token in the UI is close to the model's first-token latency, not the full latency.
- [ ] An event filter returns only the intended model's tokens in a multi-step chain.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 streaming how-to and concepts page: API list and the legacy astream_log note, input-stream requirement, finalised-input steps breaking streaming, generator fix, JSON partial objects, v2 version requirements, event table, naming/tag/type filters, callback propagation, custom events.
- Removed as unconfirmed: the claim that PydanticOutputParser emits only at the end, the `on_custom_event` event name, `exclude_*` filters, Claude list-of-blocks content advice and `.text`, LangGraph stream_mode details and `subgraphs=True`, the Python 3.10 config-passing gotcha, `disable_streaming`, proxy buffering header advice, and the LangGraph streaming source (not read).
Method: documentation only; no commands were run.
