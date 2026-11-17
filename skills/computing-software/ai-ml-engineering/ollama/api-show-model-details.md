---
id: computing-software.ai-ml-engineering.ollama.api-show-model-details
name: api-show-model-details
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-show, capabilities, model-info, template, apishow]
level: practitioner
status: docs-checked
description: "Inspect a model with POST /api/show: parameters, template, license, details, capabilities, model_info and thinking values."
sources:
  - https://docs.ollama.com/api-reference/show-model-details.md
  - https://docs.ollama.com/capabilities/thinking.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: discover what a model supports before calling it.

```
curl http://localhost:11434/api/show -d '{"model": "gpt-oss"}'
```

Request: `model` (required) and `verbose` (true adds large verbose fields).

Response fields include:

- `parameters`: model parameter settings as text
- `license`
- `modified_at`
- `details`: high-level model details (the example shows format, family, parameter_size, quantization_level)
- `template`: the template used to render prompts
- `renderer` and `parser`: the effective chat renderer and output parser, when set
- `template_source`: where the prompt actually comes from, one of `renderer_parser`, `renderer`, `parser`, `harmony`, `go_template`, `gguf_chat_template` or `none`
- `capabilities`: list of supported features (the example shows `completion`, `thinking`, `vision`)
- `model_info`: additional model metadata
- `thinking`: an object with `values` and `default`; omitted for models with no thinking metadata

Thinking controls vary by model. `values` can be booleans for on/off models or named levels such as `["low", "medium", "high"]`; `default` is used when `think` is unset; `values: [false]` means thinking is unsupported. Use the exact strings from `values` in `think`; unsupported names fall back to the model default.

## Checked

Method: 2026-11-08 read the full show-model-details page and the thinking capability page. Removed unsupported claims (speech capability and voices, CLI equivalents `ollama show` and `--modelfile`); added template_source values and the omitted-thinking case.
