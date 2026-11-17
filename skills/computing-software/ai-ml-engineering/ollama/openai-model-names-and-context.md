---
id: computing-software.ai-ml-engineering.ollama.openai-model-names-and-context
name: openai-model-names-and-context
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [gpt-3-5-turbo, ollama-cp, num-ctx, modelfile-context, gpt-35-turbo]
level: advanced
status: docs-checked
description: "Satisfy tools that hardcode OpenAI model names with ollama cp, and set context size via a Modelfile since the OpenAI API cannot."
sources:
  - https://docs.ollama.com/api/openai-compatibility.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make OpenAI-only tools work against Ollama.

Tools that expect default OpenAI model names such as `gpt-3.5-turbo` can be pointed at a local model by copying it to that name:

```
ollama cp llama3.2 gpt-3.5-turbo
```

Then use the new name in the `model` field:

```
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello!"}]}'
```

Context size: the OpenAI API has no way to set it. The page's fix is a Modelfile:

```
FROM <some model>
PARAMETER num_ctx <context size>
```

Then create the model with `ollama create mymodel` (from that Modelfile) and pass `mymodel` as the model name.

Through a signed-in local server, select a cloud model such as `gemma4:cloud`; with direct cloud access use the identifiers from `https://ollama.com/api/tags`, with no pull needed.

The page lists `reasoning_effort` (and `reasoning.effort`) as supported request fields with model-defined names; `tool_choice` and `logit_bias` are not supported. Vision requests use `image_url` content.

## Checked

Method: 2026-11-08 read the full OpenAI compatibility page. The ollama cp and Modelfile num_ctx steps match the page; removed the unsupported OLLAMA_CONTEXT_LENGTH alternative and the `-f` flag; added the supported-field notes.
