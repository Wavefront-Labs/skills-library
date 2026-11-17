---
id: computing-software.ai-ml-engineering.ollama.api-usage-metrics
name: api-usage-metrics
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [total-duration, eval-count, prompt-eval-count, nanoseconds]
level: practitioner
status: docs-checked
description: "Read token counts and nanosecond timings from the final chunk: total_duration, load_duration, prompt_eval_count, eval_count."
sources:
  - https://docs.ollama.com/api/usage.md
  - https://docs.ollama.com/api/generate.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: measure speed and token use per request.

Responses from endpoints that return usage metrics (generate and chat per their reference pages) include these fields; in a streamed response they appear in the final chunk where `done` is true:

- `total_duration`: how long the response took to generate.
- `load_duration`: how long the model took to load.
- `prompt_eval_count`: number of input tokens in the prompt.
- `prompt_eval_cached_count`: prompt tokens read from the cache.
- `prompt_eval_duration`: time evaluating the uncached prompt tokens.
- `eval_count`: number of output tokens.
- `eval_duration`: time generating the output tokens.

All timing values are in nanoseconds. Example non-streaming generate result: `total_duration` 174560334, `load_duration` 101397084, `prompt_eval_count` 11, `prompt_eval_cached_count` 8, `eval_count` 18, `eval_duration` 52479709, `done_reason` `stop`.

Derived (arithmetic from the definitions, not stated on the page): output tokens per second is `eval_count / eval_duration * 10^9`.

## Checked

Method: 2026-11-08 read the usage page and the generate reference in full. Removed unsupported claims (load_duration implying model not in memory, embed response fields, System One usage, cloud usage API); kept the metric list and units.
