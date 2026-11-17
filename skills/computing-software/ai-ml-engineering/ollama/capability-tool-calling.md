---
id: computing-software.ai-ml-engineering.ollama.capability-tool-calling
name: capability-tool-calling
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [tool-calling, function-calling, tool-name, agent-loop, tools]
level: advanced
status: docs-checked
description: "Implement tool calling: tools definitions, assistant tool_calls, role tool replies with tool_name, parallel calls and agent loops."
sources:
  - https://docs.ollama.com/capabilities/tool-calling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a model call your functions.

Pass `tools` to `/api/chat`:

```
curl -s http://localhost:11434/api/chat -d '{
  "model": "qwen3",
  "messages": [{"role": "user", "content": "What is the temperature in New York?"}],
  "stream": false,
  "tools": [{"type": "function", "function": {
    "name": "get_temperature",
    "description": "Get the current temperature for a city",
    "parameters": {"type": "object", "required": ["city"],
      "properties": {"city": {"type": "string", "description": "The name of the city"}}}}}]
}'
```

The assistant reply contains `tool_calls` with `function.name` and `function.arguments`. Run the function, then send a follow-up that includes the original user message, the assistant message with its `tool_calls` and a tool message:

```
{"role": "tool", "tool_name": "get_temperature", "content": "22°C"}
```

Patterns on the page:

- Single-shot: one tool call and one follow-up.
- Parallel: several `tool_calls` (each with an `index`) in one response; send all results back.
- Agent loop: repeat until no more tool calls; it can help to tell the model it is in a loop and may make multiple calls.
- Streaming: gather every chunk of `thinking`, `content` and `tool_calls`, then return them together with the tool results.

The Python SDK builds a tool schema from plain functions passed in the `tools` list.

## Checked

Method: 2026-11-08 read the full tool calling page. Removed the unsupported "64000 token context" claim; the request/reply shapes, parallel, agent-loop and streaming patterns match the page.
