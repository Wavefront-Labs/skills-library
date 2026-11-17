---
id: computing-software.ai-ml-engineering.vllm.tool-strict-mode
name: tool-strict-mode
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [tool-strict-level, strict-tools, structural-tag, vllm-enforce-strict-tool-calling]
level: advanced
status: docs-checked
description: "Constrain tool-call markup and arguments with strict:true, --tool-strict-level and VLLM_ENFORCE_STRICT_TOOL_CALLING."
sources:
  - https://docs.vllm.ai/en/latest/features/tool_calling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop malformed tool calls leaking into responses with `tool_choice="auto"`.

Structural-tag constraints have two layers. The envelope (markup and function name) is constrained whenever a structural tag applies: always for `required` and named choices, and for `auto` once at least one tool sets `strict: true` or the server raises the floor. A tool's argument schema is pinned only when that tool sets `strict: true` (or under `--tool-strict-level parameter`); a tool that omits `strict` stays unconstrained even if another tool in the request is strict. The `strict` field works on Chat Completion, Responses and Anthropic Messages APIs.

For best compatibility write parameter schemas in OpenAI strict-schema style: `additionalProperties: false` on each object, all properties required, optional fields as `{"type": ["string", "null"]}`.

Most clients never set `strict`, so the operator can raise the floor with `--tool-strict-level`:
- `auto`: follow the request's tool choice and per-tool strictness.
- `function`: constrain the envelope for every request with tools.
- `parameter`: also pin argument schemas for every tool, as if all were strict.

```bash
vllm serve ... --tool-strict-level function
```

When unset, the parser default applies: `function` for `glm47`, `auto` for other parsers; passing `--tool-strict-level auto` overrides a parser default. The floor never relaxes constraints a request already gets, and with `auto` a plain text response stays valid.

`VLLM_ENFORCE_STRICT_TOOL_CALLING` defaults to `true`. Set `false` to disable structural tags entirely; it takes precedence over `--tool-strict-level`. It does not change schema-derived structured outputs used by named calls or `required`.

Without these conditions, vLLM extracts tool calls from raw text, so arguments may occasionally violate the parameter schema.

## Checked

Method: 2026-11-08 read the vLLM tool calling page (docs source markdown) in full; Strict Mode and Server-Side Strictness Floor sections checked line by line.
Changes: added the OpenAI strict-schema style advice, the point that a non-strict tool stays unconstrained, and the parser-default override. All earlier claims were unchanged and match the page.
