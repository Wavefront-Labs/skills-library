---
id: computing-software.ai-ml-engineering.llama-cpp.server-chat-template-flags
name: server-chat-template-flags
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, chat-template, jinja, template-file, built-in-templates]
level: practitioner
status: docs-checked
description: "Choose or override the chat template with --jinja, --chat-template and --chat-template-file."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md", "https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Chat templates

- `--jinja` / `--no-jinja`: use the Jinja template engine. Enabled by default.
- `--chat-template JINJA_TEMPLATE`: custom Jinja template (default: taken from the model's metadata). Only commonly used built-in templates are accepted unless `--jinja` is set before this flag; the list includes `chatml`, `llama3`, `mistral-v1`, `gemma` and `deepseek`.
- `--chat-template-file FILE`: load a template from a file.
- `--chat-template-kwargs JSON`: extra template variables such as `{"enable_thinking": false}`.
- `--skip-chat-parsing`: leave tool calls and reasoning unparsed in `content`.
- `--prefill-assistant`: if the last message is from the assistant, prefill the response with it.

The default template is taken from the model's metadata. `GET /props` returns `chat_template`, the model's original Jinja2 template. `POST /apply-template` returns the formatted prompt in its `prompt` field without running inference.

Example override:

```bash
llama-server -m /path/to/model.gguf --jinja --chat-template-file /path/to/template.jinja
```

The function-calling docs suggest `--chat-template chatml` when there is no official tool_use Jinja template (they say it works with many models, results may vary). Env: `LLAMA_ARG_CHAT_TEMPLATE`, `LLAMA_ARG_CHAT_TEMPLATE_FILE`.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: --jinja default, --chat-template and --chat-template-file wording and built-in names, --chat-template-kwargs, --skip-chat-parsing, --prefill-assistant, GET /props chat_template, POST /apply-template and the env variables; in the function-calling doc the chatml tip. Reworded: the acceptance rule for built-in templates and the chatml fallback.

Method: docs-only read of cited pages, 2026-11-08
