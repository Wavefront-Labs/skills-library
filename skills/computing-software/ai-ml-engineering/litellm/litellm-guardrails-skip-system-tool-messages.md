---
id: computing-software.ai-ml-engineering.litellm.litellm-guardrails-skip-system-tool-messages
name: litellm-guardrails-skip-system-tool-messages
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, guardrails, skip-system-message, skip-tool-message]
level: advanced
status: docs-checked
description: "Exclude system or tool messages from guardrail scans with skip_system_message_in_guardrail and skip_tool_message_in_guardrail."
sources:
  - https://docs.litellm.ai/docs/proxy/guardrails/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop guardrails scanning `role: system` or `role: tool` content while still sending the full messages list to the model.

Global, in litellm_settings:

```
litellm_settings:
  skip_system_message_in_guardrail: true
  skip_tool_message_in_guardrail: true
```

Per guardrail, set the same keys to `true` or `false` under that guardrail's `litellm_params`. If omitted, the global value is used; a per-guardrail `false` forces those messages back into the scan even when the global flag skips them.

Admin UI: the guardrail form has a Skip system messages and a Skip tool messages dropdown with three options: Use global default, Yes (exclude from the scan, per-guardrail true) and No (always include, per-guardrail false).

Anthropic /v1/messages: since v1.103.0, guardrails also scan the top-level `system` prompt there. Claude Desktop and Cowork send a long system prompt with every request, which a strict prompt-attack filter can trip. On /v1/messages the skip flag skips only the top-level system prompt; a `role: system` entry inside `messages` is client input, so guardrails scan it even with the flag set.

Where the flags apply: the unified guardrail path, meaning providers that implement `apply_guardrail` and run through LiteLLM's message translation, on /v1/chat/completions and Anthropic /v1/messages.

Where they do not apply: guardrails that run only through direct hooks on the raw request, such as Aporia, DynamoAI, Javelin, Lasso, Pangea, Model Armor, Azure Content Safety hooks and Guardrails AI.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/guardrails/quick_start (skip system and tool message sections)