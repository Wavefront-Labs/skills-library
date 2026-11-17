---
id: computing-software.ai-ml-engineering.vllm.structured-outputs
name: structured-outputs
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [structured-outputs, guided-decoding, xgrammar, guidance, json-schema, structural-tag]
level: practitioner
status: docs-checked
description: "Constrain generation to choices, regex, JSON schema, grammar or structural tags with the xgrammar or guidance backend."
sources:
  - https://docs.vllm.ai/en/latest/features/structured_outputs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: force model output to follow a format you specify.

Backends are xgrammar and guidance. Select with `--structured-outputs-config.backend`; the default is `auto`, which picks a backend per request. The lm-format-enforcer backend is deprecated from v0.33.0 (opt-in required in v0.34.0, removed in v0.35.0); migrate to `auto`.

Constraint types (request parameters):
- `choice`: output is one of a list of strings.
- `regex`: output matches a regular expression.
- `json`: output follows a JSON schema (for example from a Pydantic model).
- `grammar`: output follows a context-free grammar.
- `structural_tag`: follow a JSON schema within a set of specified tags in the generated text.

For the OpenAI-compatible server, these are passed through the request's structured-output fields. The old `guided_*` request fields were removed in v0.12.0; use the structured outputs parameters instead.

Qwen3 Coder with reasoning enabled (v0.11.2+): structured outputs may become disabled if reasoning is not parsed into the `reasoning` field separately. To use both, start the server with `--structured-outputs-config.enable_in_reasoning=True`. Custom grammars must also include the boundary tokens the configured reasoning or tool parser expects.

Experimental automatic parsing: the OpenAI client's `client.beta.chat.completions.parse` wrapper lets you pass Pydantic types and get parsed objects back.

## Checked

2026-11-03. Confirmed against the Structured Outputs page (docs.vllm.ai/en/latest/): backends, default auto, constraint types, removed guided fields, lm-format-enforcer deprecation timeline and enable_in_reasoning. Corrected the structural_tag description and the beta parse call; removed an unconfirmed claim about grammar compilation latency and tool_choice.

Method: documentation only; no commands were run.
