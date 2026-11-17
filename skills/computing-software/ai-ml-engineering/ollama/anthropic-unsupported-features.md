---
id: computing-software.ai-ml-engineering.ollama.anthropic-unsupported-features
name: anthropic-unsupported-features
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [tool-choice, count-tokens, prompt-caching, budget-tokens]
level: advanced
status: docs-checked
description: "Know what the Ollama Anthropic API does not support: tool_choice, count_tokens, caching, batches, citations, PDFs and URL images."
sources:
  - https://docs.ollama.com/api/anthropic-compatibility.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid features that silently will not work.

The Anthropic compatibility page lists these as not currently supported:

- `/v1/messages/count_tokens` (token counting)
- `tool_choice` (forcing or disabling specific tools)
- `metadata` (request user_id)
- prompt caching (`cache_control` blocks)
- the Batches API (`/v1/messages/batches`)
- citations content blocks
- PDF support (`document` content blocks)
- server-sent `error` events during streaming (errors return an HTTP status instead). Note the same page also ticks `error` in its streaming events checklist, so the two statements disagree; test before relying on either.

Partial support:

- Images: base64 is supported, URL images are not.
- Extended thinking: basic support; `budget_tokens` is accepted but not enforced.

Behaviour differences:

- The local server does not validate API keys; direct cloud inference requires a valid bearer token.
- The hosted endpoint rejects `anthropic-version` values older than `2023-06-01`.
- Token counts are approximations based on the underlying model's tokenizer.

Tool-choice controls, deferred tools and hosted web search are not fully supported on the direct cloud endpoint, per the page's cloud section. Supported: messages, streaming, system prompts, multi-turn, vision (base64), tools and tool results, thinking, `output_config.effort` with model-defined names.

## Checked

Method: 2026-11-08 read the full Anthropic compatibility page. Not-supported, partial-support and behaviour-difference lists match the page; removed the unsupported "practical impact" advice and flagged the page's internal inconsistency about streaming error events.
