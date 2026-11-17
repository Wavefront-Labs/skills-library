---
id: computing-software.ai-ml-engineering.vllm.reasoning-outputs
name: reasoning-outputs
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [reasoning-parser, reasoning-outputs, reasoning-content, enable-thinking, include-reasoning]
level: practitioner
status: docs-checked
description: "Extract reasoning with --reasoning-parser, set thinking defaults, map efforts, and hide reasoning."
sources:
  - https://docs.vllm.ai/en/latest/features/reasoning_outputs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: return a model's chain of thought separately from its final answer.

Start the server with `--reasoning-parser`, for example `vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B --reasoning-parser deepseek_r1`. Reasoning is available only on `/v1/chat/completions`, the Anthropic Messages API (`/v1/messages`) and the Responses API (`/v1/responses`).

Server-wide thinking defaults use `--default-chat-template-kwargs`:
- Disable for Qwen3: `--reasoning-parser qwen3 --default-chat-template-kwargs '{"enable_thinking": false}'`.
- Enable for Granite 3.2: `--reasoning-parser granite --default-chat-template-kwargs '{"thinking": true}'`.

Request-level `chat_template_kwargs` in `extra_body` always override server defaults.

`reasoning_effort` (Chat Completions) or `reasoning.effort` (Responses) auto-injects `enable_thinking`: low, medium or high gives true, `none` gives false, unset injects nothing. An explicit `enable_thinking` wins.

`--reasoning-effort-map` rewrites client efforts into values a template recognizes, e.g. `'{"minimal": "low", "medium": "low", "xhigh": "max"}'`. Keys must be none, minimal, low, medium, high, xhigh or max; unlisted efforts pass through, and a `reasoning_effort` placed directly in `chat_template_kwargs` is not rewritten.

`include_reasoning=false` still generates reasoning tokens but omits them from responses, and also suppresses logprobs and token IDs so reasoning cannot leak.

## Checked

2026-11-03. Confirmed against the Reasoning Outputs page (docs.vllm.ai/en/latest/): endpoint limits, default chat template kwargs, reasoning_effort injection, effort map and include_reasoning.

Method: documentation only; no commands were run.
