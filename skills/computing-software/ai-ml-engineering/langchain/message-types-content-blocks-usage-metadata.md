---
id: computing-software.ai-ml-engineering.langchain.message-types-content-blocks-usage-metadata
name: message-types-content-blocks-usage-metadata
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, usage-metadata, content-blocks, aimessage, toolmessage, message-types, tool-calls]
level: practitioner
status: verified
description: "Work with LangChain messages: System/Human/AI/Tool types, AIMessage.tool_calls, string vs block content, usage_metadata token counts and chunk merging."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Message types, content blocks and usage_metadata

## Types
| Class | Role | Notable fields |
|---|---|---|
| `SystemMessage` | system | instructions |
| `HumanMessage` | user | text or multimodal blocks |
| `AIMessage` | assistant | `content`, `tool_calls`, `usage_metadata`, `response_metadata`, `id` |
| `ToolMessage` | tool result | `tool_call_id` (must match), `content`, optional `artifact`, `status` |
| `AIMessageChunk` | streaming piece | `+` merges chunks (run: `AIMessageChunk("a") + AIMessageChunk("b")` gives content `"ab"`) |

## content: str or list of blocks
Providers with reasoning, citations or tool use return a list of blocks (`[{"type": "text", ...}, {"type": "tool_use", ...}]`). Use `msg.text` (a property in langchain-core 1.6.12; run: joined two text blocks as `"ab"`) to get concatenated text safely; `msg.content_blocks` exposes a provider-normalized standard view in LangChain 1.x.

## Tool-call round trip
```python
ai = llm_tools.invoke(messages)
messages.append(ai)
for tc in ai.tool_calls:
    result = tools_by_name[tc["name"]].invoke(tc["args"])
    messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
final = llm_tools.invoke(messages)
```
Every tool call needs a matching ToolMessage before the next model call; missing ones cause provider errors.

## Token usage
```python
ai.usage_metadata   # {'input_tokens': 812, 'output_tokens': 95, 'total_tokens': 907,
                    #  'input_token_details': {'cache_read': 640, 'cache_creation': 0}, ...}
```
- Aggregate across a run with `from langchain_core.callbacks import get_usage_metadata_callback` (`with get_usage_metadata_callback() as cb: ...; cb.usage_metadata`; `UsageMetadataCallbackHandler` is the underlying handler). The result is a dict keyed by model name taken from `response_metadata["model_name"]` (run: `{"fake-1": {...}}`; a message without a model name gave `{}`).
- When streaming, usage arrives on the final chunk (some providers need `stream_usage=True`).
- `response_metadata` carries the provider's raw fields: model name, stop reason, request ids.

## Serialization
`messages_to_dict` / `messages_from_dict`, or `.model_dump()`; store messages this way for conversation persistence.

## Verify
- [ ] Logged token counts per request match the provider dashboard over a sample.
