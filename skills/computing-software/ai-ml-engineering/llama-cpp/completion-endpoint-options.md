---
id: computing-software.ai-ml-engineering.llama-cpp.completion-endpoint-options
name: completion-endpoint-options
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, completion-endpoint, n-predict, stop-strings, sampling]
level: practitioner
status: docs-checked
description: "The native POST /completion endpoint: accepted prompt shapes and the main request fields with defaults."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# POST /completion

This native endpoint is not OpenAI-compatible; use `/v1/completions` for OAI clients.

**`prompt` shapes:** a single string, a token sequence such as `[12, 34, 56]`, a mix like `[12, 34, "string", 56, 78]`, or an object `{ "prompt_string": "string", "multimodal_data": ["base64"] }`. An array of several prompts returns an array of results. A BOS token is inserted only if the prompt is a string (or an array whose first element is a string) and the model's `tokenizer.ggml.add_bos_token` metadata is true. With `cache_prompt` true, the prompt is compared with the previous completion and only the unseen suffix is evaluated. For `multimodal_data`, the string prompt needs the same number of MTMD media markers (for example `<__media__>`) as placeholders, and clients should check `/models` or `/v1/models` for multimodal capability first.

Key fields and defaults:

- `n_predict`: -1 (infinity); may exceed the limit slightly if the last token is a partial multibyte character; `0` evaluates the prompt into the cache without generating.
- `n_keep`: 0; the number of prompt tokens kept when the context is exceeded (excludes BOS); `-1` keeps all.
- `stop`: JSON array of stop strings, default `[]`; the stop words are not included in the completion.
- `temperature` 0.8, `top_k` 40, `top_p` 0.95, `min_p` 0.05, `typical_p` 1.0 (disabled), `repeat_penalty` 1.1, `repeat_last_n` 64 (0 disables), `presence_penalty` and `frequency_penalty` 0.0 (disabled).
- DRY: `dry_multiplier` 0.0 (disabled), `dry_base` 1.75, `dry_allowed_length` 2, `dry_penalty_last_n` 64, `dry_sequence_breakers` default `['\n', ':', '"', '*']`. XTC: `xtc_probability` 0.0, `xtc_threshold` 0.1. Mirostat: `mirostat` 0 (1 = Mirostat, 2 = Mirostat 2.0), `mirostat_tau` 5.0, `mirostat_eta` 0.1.
- `seed`: -1 means a random seed. `ignore_eos`: false.
- `cache_prompt`: true; can cause nondeterministic results because logits are not guaranteed bit-for-bit identical across batch sizes.
- `n_cmpl`: number of completions to generate from the prompt.
- `n_cache_reuse`: minimum chunk size to reuse from the cache via KV shifting, default 0 (disabled).
- `id_slot`: -1 assigns the task to an idle slot.
- `t_max_predict_ms`: time limit in ms for the generation phase, measured from the first token and triggering only once a newline has been generated; default 0 (disabled); useful for FIM.
- `n_indent`: minimum line indentation of generated text in whitespace characters, default 0.
- `n_probs`: if above 0, the response also contains the probabilities of the top N tokens; `post_sampling_probs` returns probabilities after the sampling chain.
- `samplers`: order of samplers, default `["dry", "top_k", "typ_p", "top_p", "min_p", "xtc", "temperature"]`.
- `logit_bias`: for example `[[15043,1.0]]`; a `false` value bans the token.
- `response_fields`: list of fields to keep, for example `["content", "generation_settings/n_predict"]`; missing fields are omitted without error and slashed fields are unnested.
- `return_tokens`, `timings_per_token`, `return_progress`, `sse_ping_interval`: see the streaming skill.

`grammar` and `json_schema` constrain output. `lora` takes `[{"id": 0, "scale": 0.5}]`; adapters not listed default to scale 0.0, and requests with different LoRA configurations are not batched together.

## Checked

Date: 2026-11-08. Confirmed against the POST /completion section of the llama-server README. Added the documented defaults for the DRY, XTC, Mirostat and sampler-order fields; no claims were removed.

Method: docs-only read of cited pages, 2026-11-08
