---
id: computing-software.ai-ml-engineering.llama-cpp.server-props-endpoint
name: server-props-endpoint
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, props-endpoint, server-properties, chat-template, modalities]
level: practitioner
status: docs-checked
description: "Read global server properties from GET /props and when POST /props is allowed."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GET /props

Returns global server properties. It is read-only by default; starting the server with `--props` allows `POST /props` (its options list is "None yet").

Response fields:

- `default_generation_settings`: the defaults for `/completion`, with the same fields as the `generation_settings` object of `/completion` (includes `n_ctx`, sampler `params`, `samplers`, and `speculative.*` values).
- `total_slots`: number of slots for processing requests, defined by `--parallel`.
- `model_path`: path to the model file, same as the `-m` argument.
- `chat_template`: the model's original Jinja2 prompt template.
- `chat_template_caps`: capabilities of the chat template; `reasoning_effort_levels` lists the `reasoning_effort` values the template renders distinctly, from lowest to highest.
- `modalities`: supported modalities, for example `{"vision": false}`.
- `media_marker`: the placeholder string used in multimodal prompts (the example response shows it).
- `voices`: predefined voices of an audio generation model, to pass as `voice` to `/tts`; present only when the model has some.
- `build_info`: build number and commit hash.
- `is_sleeping`: sleeping status (see the "Sleeping on Idle" section; `GET /props` does not wake the model or reset the idle timer).

In router mode query `GET /props?model=<url-encoded model name>`, for example `/props?model=ggml-org%2Fgemma-3-4b-it-GGUF%3AQ4_K_M`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the llama.cpp server README sections `GET /props`, `POST /props`, router mode and Sleeping on Idle. Removed: the `chat_template_tool_use` field and the advice to use it to check tool support, which the page does not mention.
