---
id: computing-software.ai-ml-engineering.ollama.context-length-defaults
name: context-length-defaults
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [context-length, vram, default-context, 64k, contextlength]
level: practitioner
status: docs-checked
description: "Understand how Ollama picks a default context window from VRAM and when to raise it to at least 64000 tokens."
sources:
  - https://docs.ollama.com/context-length.md
  - https://docs.ollama.com/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid truncated context in agents and search tools.

Context length is the maximum number of tokens the model keeps in memory. The context-length page states defaults by available VRAM:

- under 24 GiB: 4k context
- 24 to 48 GiB: 32k context
- 48 GiB or more: 256k context

Guidance: tasks such as web search, agents and coding tools should use a context window of at least 64000 tokens. Cloud models default to their maximum context length.

Set it for the server:

```
OLLAMA_CONTEXT_LENGTH=64000 ollama serve
```

The app has a context length slider in its settings. Verify the effective value with `ollama ps` (CONTEXT column) and the PROCESSOR column to see whether the larger window pushed the model partly onto the CPU.

Memory impact from the FAQ: the RAM needed for parallel requests scales as `OLLAMA_NUM_PARALLEL` times `OLLAMA_CONTEXT_LENGTH`, because each parallel request gets its own context. Raising both can stop a model from fitting in VRAM.

Discrepancy: the FAQ example text calls the default 4096 tokens and the Modelfile page lists `num_ctx` 2048; the context-length page, which gives the VRAM table, is the most specific, so check `ollama ps` rather than assuming.

## Checked

2026-11-03. VRAM-based defaults, 64000 guidance, cloud default and `ollama ps` against the context-length page; 4096 FAQ text and the parallel-memory formula against the FAQ (docs.ollama.com/faq); `num_ctx` 2048 against the Modelfile reference (docs.ollama.com/modelfile). Nothing removed.

Method: documentation only; no commands were run.
