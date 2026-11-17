---
id: computing-software.ai-ml-engineering.ollama.context-length-setting
name: context-length-setting
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [num-ctx, options, set-parameter, request-options]
level: practitioner
status: docs-checked
description: "Set context per session, request or model with /set parameter num_ctx, the options.num_ctx API field or a Modelfile PARAMETER."
sources:
  - https://docs.ollama.com/context-length.md
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/modelfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right scope for a context setting.

Four scopes are documented:

1. Server default: `OLLAMA_CONTEXT_LENGTH=64000 ollama serve` (or the app slider).
2. Interactive session: inside `ollama run`, type `/set parameter num_ctx 4096`.
3. API request: pass `options` with `num_ctx`:

```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "options": {"num_ctx": 4096}
}'
```

4. Model definition: `PARAMETER num_ctx 4096` in a Modelfile, then `ollama create`.

Memory warning from the FAQ: parallel requests multiply the context size. With `OLLAMA_NUM_PARALLEL` set above 1 the total context memory is parallel requests times context length, so size them together.

For cloud models the context defaults to the model maximum, so these settings matter for local models.

## Checked

2026-11-03. `/set parameter num_ctx`, the API `num_ctx` option, `OLLAMA_CONTEXT_LENGTH`, and the parallel memory formula against the FAQ (docs.ollama.com/faq) and the context-length page; Modelfile `PARAMETER num_ctx` against the Modelfile reference (docs.ollama.com/modelfile). Removed the `ModelOptions` and `load_duration` claims (API reference not fetched).

Method: documentation only; no commands were run.
