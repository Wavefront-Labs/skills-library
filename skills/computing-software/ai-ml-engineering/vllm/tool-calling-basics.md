---
id: computing-software.ai-ml-engineering.vllm.tool-calling-basics
name: tool-calling-basics
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [tool-calling, enable-auto-tool-choice, tool-call-parser, tool-choice, function-calling]
level: practitioner
status: docs-checked
description: "Enable auto tool choice with a parser, and use named, required and none tool_choice values."
sources:
  - https://docs.vllm.ai/en/latest/features/tool_calling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve function calling over the chat completion API.

vLLM supports named function calling plus `auto`, `required` (vllm>=0.8.3) and `none` for `tool_choice`.

Auto tool choice needs flags at startup:
- `--enable-auto-tool-choice`: mandatory.
- `--tool-call-parser`: the parser to use (hermes, mistral, llama3_json, pythonic and others).
- `--chat-template`: optional. The path to a template that handles `tool`-role messages and assistant messages holding earlier tool calls. Hermes, Mistral and Llama models carry tool-compatible templates in `tokenizer_config.json`; the value `tool_use` selects a tool-specific template configured there.

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --enable-auto-tool-choice --tool-call-parser llama3_json \
  --chat-template examples/tool_chat_template_llama3.1_json.jinja
```

Choices:
- Named function: `tool_choice={"type": "function", "function": {"name": "get_weather"}}`. It uses the structured outputs backend, so the first call pays seconds of latency while the FSM compiles, then it is cached. You get a validly parsable call, not a high-quality one; state the expected schema in the prompt too.
- `required`: the model is guaranteed to emit one or more tool calls from the `tools` list; the count depends on the query. Recent Mistral models in official format are an exception.
- `none`: no tool calls, regular text only. Tool definitions are still placed in the prompt unless you pass `--exclude-tools-when-tool-choice-none`.

The caller must define tools in the request, include context in the messages and run the returned calls in application code. For parallel calls and model-specific parsers see the per-model sections of the page. If your model has no parser, contribute a parser and a tool-use chat template.

## Checked

Method: 2026-11-08 read the vLLM tool calling page (docs source markdown) in full and compared each claim.
Changes: made the example command include the chat template the page uses, described what `--chat-template` does, and added the named-call quality caveat and caller responsibilities. Other claims were unchanged and match the page.
