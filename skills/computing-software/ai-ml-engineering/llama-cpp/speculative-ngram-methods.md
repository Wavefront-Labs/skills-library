---
id: computing-software.ai-ml-engineering.llama-cpp.speculative-ngram-methods
name: speculative-ngram-methods
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, ngram-mod, ngram-simple, ngram-map-k, draftless]
level: advanced
status: docs-checked
description: "Use draftless n-gram speculative decoding methods and their size defaults."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# N-gram speculative decoding

These methods need no draft model; they search the token history for patterns that already appeared and use the matching sequence as the draft (for example rewriting source code).

Choose with `--spec-type` (a comma-separated list):

- `ngram-simple`: finds the last n-gram in history matching the current one and drafts the m tokens that followed it.
- `ngram-map-k`: looks up the current n-gram (the key); if the same m tokens followed it several times, drafts them. Needs `--spec-ngram-map-k-min-hits` occurrences (default 1).
- `ngram-map-k4v`: experimental; tracks up to four values per key and drafts the dominant one.
- `ngram-mod`: a rolling hash maps each n-gram to the next token; about 16 MB, constant memory, variable draft length, and one hash pool shared across all server slots. Defaults: `--spec-ngram-mod-n-match` 24, `-n-min` 48, `-n-max` 64. Enabled by `--spec-default`.
- `ngram-cache`: keeps statistics of short n-gram sequences and drafts from the probabilities derived from them; external statistics can be loaded from files.

For `ngram-simple`, `ngram-map-k` and `ngram-map-k4v` the defaults are size-n 12 (lookup n-gram length), size-m 48 (draft m-gram length) and min-hits 1, set with `--spec-ngram-simple-size-n`/`-size-m`/`-min-hits` (and `--spec-ngram-map-k-...`, `--spec-ngram-map-k4v-...`).

```bash
llama-server [...] --spec-default
llama-server [...] --spec-type ngram-simple --spec-draft-n-max 64
llama-server [...] --spec-type ngram-mod,ngram-map-k4v
```

The page notes small `n` are not recommended for `ngram-mod` and that MoE models require long drafts. If a draft model is combined with a draftless method, the draftless method takes precedence. The llama-server metrics `llamacpp:spec_decode_num_accepted_tokens_total` and `llamacpp:spec_decode_num_draft_tokens_total` track acceptance, and each implementation also prints statistics (draft acceptance rate, `#gen tokens`, `#acc tokens`).

## Checked

2026-11-04: confirmed against the llama.cpp `speculative.md` page (n-gram sections, parameter defaults, precedence, statistics) and the llama-server README metrics list. Removed the claim that these methods "help most with code editing" beyond the page's code-rewriting example, the "almost no memory cost" closing line, and the `--metrics` requirement (not confirmed here).
Method: documentation only; no commands were run.
