---
id: computing-software.ai-ml-engineering.ollama.modelfile-parameters-defaults
name: modelfile-parameters-defaults
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [num-ctx, temperature, top-k, top-p, parameter]
level: practitioner
status: docs-checked
description: "Tune sampling and limits with PARAMETER: num_ctx, temperature, top_k, top_p, min_p, repeat_penalty, stop, num_predict and seed."
sources:
  - https://docs.ollama.com/modelfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set generation defaults baked into a model.

Syntax: `PARAMETER <name> <value>`. Documented parameters and their stated defaults:

- `num_ctx`: context window in tokens; the Modelfile page lists 2048.
- `repeat_last_n`: how far back to look to prevent repetition; default 64, `0` disables, `-1` means `num_ctx`.
- `repeat_penalty`: default 1.0.
- `temperature`: default 0.8; higher is more creative.
- `seed`: default 0; a fixed number makes output reproducible for the same prompt.
- `stop`: a stop sequence; can be given several times for several sequences.
- `num_predict`: maximum tokens to generate; default -1.
- `top_k`: default 40.
- `top_p`: default 0.9.
- `min_p`: default 0.0.
- `draft_num_predict`: tokens a draft model proposes per step; separate draft models default to 4 and `0` disables it.

```
PARAMETER temperature 1
PARAMETER num_ctx 4096
PARAMETER stop "<|end|>"
PARAMETER stop "User:"
```

Conflict to know: the context-length page says the server default is chosen from VRAM (4k below 24 GiB), so a `num_ctx` in the Modelfile pins the value for that model.

Runtime override: `/set parameter num_ctx 4096` in `ollama run`, or `options` in an API request.

## Checked

2026-11-03. Parameter names and defaults, `stop` repetition and the `draft_num_predict` behaviour confirmed against the Modelfile reference (docs.ollama.com/modelfile); the 4k-below-24-GiB server default against the context-length page. Nothing removed.

Method: documentation only; no commands were run.
