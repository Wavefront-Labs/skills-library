---
id: computing-software.ai-ml-engineering.vllm.tool-parser-plugin
name: tool-parser-plugin
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [tool-parser-plugin, toolparsermanager, register-lazy-module, custom-tool-parser]
level: advanced
status: docs-checked
description: "Register a custom tool parser with --tool-parser-plugin and select it by name in --tool-call-parser."
sources:
  - https://docs.vllm.ai/en/latest/features/tool_calling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add tool-call parsing for a model vLLM does not support yet.

`--tool-parser-plugin` is an optional flag naming a plugin file that registers user-defined tool parsers. The registered parser name can then be given to `--tool-call-parser`. The docs also invite contributing a parser plus a tool-use chat template upstream if your model is missing.

A plugin is a Python file with one or more `ToolParser` subclasses, modelled on `Hermes2ProToolParser` (`vllm/tool_parsers/hermes_tool_parser.py`). The page's skeleton implements:
- `adjust_request`: tweak the request, for example set skip special tokens to False for tool call output.
- `extract_tool_calls_streaming`: parse for streaming calls.
- `extract_tool_calls`: parse for non-stream calls, returning `ExtractedToolCallInformation`.

Registration uses `ToolParserManager.register_lazy_module(name=..., module_path=..., class_name=...)`; the name is what `--tool-call-parser` accepts.

Startup pattern (the page asks for the absolute path of the plugin file):

```bash
vllm serve <model> \
  --enable-auto-tool-choice \
  --tool-parser-plugin <absolute path of plugin file> \
  --tool-call-parser my_parser \
  --chat-template <your chat template>
```

Related built-in options on the same page:
- `hf` parser: reads the checkpoint tokenizer's `response_template` metadata instead of a model-specific parser. Use it with `--reasoning-parser hf`. Startup fails when the tokenizer lacks a `response_template` or the needed `thinking` or `tool_calls` field. It cannot be combined with other parsers and rejects strict tools, required or named choice, and `parallel_tool_calls=false`, since it provides parsing only.
- `beam` parser: reads the same metadata but also derives a structural-tag grammar from the template, so it constrains output.

If a custom structured-output grammar includes reasoning or tool-call delimiters, its token constraints must match the configured parser; see the structured outputs page on custom grammars and parser boundary tokens.

## Checked

Method: 2026-11-08 read the vLLM tool calling page (docs source markdown) in full, including the "How to Write a Tool Parser Plugin" section.
Changes: replaced the vague registration description with the three methods and the register_lazy_module arguments from the page's skeleton, added the chat-template flag, and corrected the grammar caveat to refer to custom structured-output grammars. The hf and beam notes were unchanged.
