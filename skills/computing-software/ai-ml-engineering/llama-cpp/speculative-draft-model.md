---
id: computing-software.ai-ml-engineering.llama-cpp.speculative-draft-model
name: speculative-draft-model
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, speculative-decoding, draft-model, spec-draft, draft-simple]
level: advanced
status: docs-checked
description: "Configure draft-model speculative decoding with --spec-type draft-simple and the spec-draft flags."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Speculative decoding with a draft model

A much smaller draft model generates draft tokens, which the target model verifies in a single batch; this speeds up generation when the drafts are often right.

```bash
llama-server -m /path/to/target.gguf -md /path/to/draft.gguf --spec-type draft-simple
```

Flags (from the page):

- `--spec-draft-model, -md, --model-draft FNAME`: the draft model; `--spec-draft-hf, -hfd` takes a Hugging Face `<user>/<model>[:quant]`.
- `--spec-type`: `none` (default), `draft-simple`, `draft-eagle3`, `draft-dflash`, `draft-dspark`, `draft-mtp`, `ngram-cache`, `ngram-simple`, `ngram-map-k`, `ngram-map-k4v`, `ngram-mod`. It takes a comma-separated list, so draft and draftless types can be mixed.
- `--spec-draft-n-max N`: tokens to draft, default 3.
- `--spec-draft-n-min N`: minimum draft tokens, default 0.
- `--spec-draft-p-min P`: minimum speculative decoding probability (greedy), default 0.00.
- `--spec-draft-p-split P`: split probability, default 0.10.
- `-ngld, --spec-draft-ngl N`: draft layers in VRAM (exact number, `auto` or `all`; default auto); `-devd, --spec-draft-device`: devices for the draft model.
- `--spec-draft-n-ubatch N`: draft context physical batch size; a smaller value spares VRAM.
- `--spec-default`: default speculative config; it enables `ngram-mod`.

If a draft model is combined with a draftless method, the draftless method has higher precedence. `--spec-synth-rates` and `--spec-synth-len` replace verification with synthetic decisions for benchmarking; output is then not valid model output.

## Checked

2026-11-04: confirmed against the llama.cpp `speculative.md` page (command-line option listings, `--spec-type` table, precedence, synthetic acceptance). Removed `--spec-draft-sampling` (not in the docs), the `GET /slots` acceptance claim, the vocabulary-compatibility and "no quality change" statements.
Method: documentation only; no commands were run.
