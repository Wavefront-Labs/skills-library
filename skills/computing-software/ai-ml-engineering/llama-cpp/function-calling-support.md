---
id: computing-software.ai-ml-engineering.llama-cpp.function-calling-support
name: function-calling-support
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, function-calling, tool-calls, jinja, tool-templates]
level: practitioner
status: docs-checked
description: "Enable tool calling with --jinja, native format handlers, the generic fallback and template overrides."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md", "https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Function calling

OpenAI-style function calling is implemented in `chat.h` and used by llama-server when started with `--jinja` (the llama-cli README lists `--jinja` as enabled by default; the function-calling guide's examples all pass it explicitly). Send `tools` in a `/v1/chat/completions` request.

Native tool-call formats named on the page: Llama 3.1 / 3.3 (including builtin tools: wolfram_alpha, web_search / brave_search, code_interpreter) and Llama 3.2; Functionary v3.1 / v3.2; Hermes 2/3 and Qwen 2.5 (also Qwen 2.5 Coder); Mistral Nemo; Firefunction v2; Command R7B; DeepSeek R1 (marked WIP, "seems reluctant to call any tools?"); GPT-OSS (Harmony) and LLM-jp-4.1 (Harmony dialect).

When the template is not recognised by a native handler, the Generic format is used (the logs show `Chat format: Generic`). Generic support may consume more tokens and be less efficient than a model's native format.

Checks and fixes:

- Start with any model, but confirm its template supports tools by inspecting the `chat_template` or `chat_template_tool_use` properties from the server's `/props` endpoint.
- Override with `--chat-template-file`. Examples from the page: `models/templates/llama-cpp-deepseek-r1.jinja` for DeepSeek R1 distills (the official template is buggy, although the code works around it), `models/templates/meetkai-functionary-medium-v3.2.jinja` for Functionary, `models/templates/NousResearch-Hermes-2-Pro-Llama-3-8B-tool_use.jinja` for Hermes 2 Pro. `scripts/get_chat_template.py` fetches official templates from Hugging Face repos.
- If there is no official `tool_use` template, `--chat-template chatml` may work for many models ("YMMV").
- Multiple/parallel tool calling works on some models but is disabled by default; enable it with `"parallel_tool_calls": true` in the request payload.
- Extreme KV quantization (for example `-ctk q4_0`) can substantially degrade tool-calling performance.

Example launch and request from the page:

```bash
llama-server --jinja -fa -hf bartowski/Qwen2.5-7B-Instruct-GGUF:Q4_K_M

curl http://localhost:9931/v1/chat/completions -d '{"messages":[{"role":"user","content":"Weather in Istanbul?"}],
 "tools":[{"type":"function","function":{"name":"get_current_weather","parameters":{"type":"object","properties":{"location":{"type":"string"}},"required":["location"]}}}]}'
```

`--skip-chat-parsing` (llama-cli README) forces a pure content parser: the model's output, including reasoning and tool calls, stays in the content section.

## Checked

Date: 2026-11-08. Confirmed against docs/function-calling.md and the `--jinja` and `--skip-chat-parsing` entries of the llama-cli README. Corrected: the handler list (page names Llama 3.x, Functionary, Hermes 2/3, Qwen 2.5, Mistral Nemo, Firefunction v2, Command R7B, DeepSeek R1, GPT-OSS; removed the unsupported "best results" claim) and the `/props` check wording; removed `--chat-template chatml` as an unconditional fallback.

Method: docs-only read of cited pages, 2026-11-08
