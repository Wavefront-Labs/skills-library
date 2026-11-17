---
id: computing-software.ai-ml-engineering.llama-cpp.server-reasoning-controls
name: server-reasoning-controls
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, reasoning, thinking-budget, reasoning-format, reasoning-effort]
level: practitioner
status: docs-checked
description: "Control thinking output with reasoning, reasoning-format, effort, budget flags and the realtime control endpoint."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md", "https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reasoning controls

Flags (shared by llama-server and llama-cli):

- `-rea, --reasoning [on|off|auto]`: default `auto`, detected from the template.
- `--reasoning-format`: `none` leaves thoughts in `message.content`; `deepseek` puts them in `message.reasoning_content`; `deepseek-legacy` keeps tags in content and also fills `reasoning_content`. Default auto.
- `--reasoning-effort LEVEL`: `default` keeps the template default; or `minimal`, `low`, `medium`, `high`, `xhigh`, `max`.
- `--reasoning-budget N`: -1 unrestricted (default), 0 end immediately, N above 0 a token budget.
- `--reasoning-budget-message MESSAGE`: injected before the end-of-thinking tag when the budget runs out.
- `--reasoning-preserve`: keep the reasoning trace in the full history, for templates with `supports_preserve_reasoning`.
- `--chat-template-kwargs '{"enable_thinking": false}'` passes template variables.
- `--skip-chat-parsing`: output everything, reasoning and tool calls included, in `content`.

Per request on `/v1/chat/completions`: `reasoning_effort` (`none` disables thinking), `reasoning_format`, `chat_template_kwargs`.

Ending thinking early: send `"reasoning_control": true` with the request, then `POST /v1/chat/completions/control` with `{"id": "<completion id>", "action": "reasoning_end"}` while streaming. Include `model` in router mode. It returns `{"success": true}` or a `message` on failure; a finished completion is a no-op.

## Checked

2026-11-08. Confirmed in the llama.cpp server README and the llama-cli README: the reasoning flags, formats, effort levels, budget values and defaults; in the server README the per-request reasoning_effort, reasoning_format, chat_template_kwargs and reasoning_control fields and the POST /v1/chat/completions/control endpoint (id, action reasoning_end, model in router mode, success and message response). Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
