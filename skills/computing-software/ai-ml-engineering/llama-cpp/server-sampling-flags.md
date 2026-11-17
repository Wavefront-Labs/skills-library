---
id: computing-software.ai-ml-engineering.llama-cpp.server-sampling-flags
name: server-sampling-flags
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, sampling, sampler-order, top-k, min-p]
level: practitioner
status: docs-checked
description: "Default sampler chain and the main sampling flags with their default values."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sampling flags

Default sampler order: `penalties;dry;top_n_sigma;top_k;typ_p;top_p;min_p;xtc;temperature`.

- `--samplers LIST`: samplers separated by `;`. `--sampler-seq SEQ`: short form, default `edskypmxt`.
- `-s, --seed`: -1 random.
- `--temp` 0.8; `--top-k` 40 (0 disables); `--top-p` 0.95 (1.0 disables); `--min-p` 0.05 (0.0 disables).
- `--repeat-last-n` 64 (0 disables); `--repeat-penalty` 1.0 (disabled); `--presence-penalty` and `--frequency-penalty` 0.0.
- `--typical` 1.0; `--top-nsigma` -1 (disabled).
- `--xtc-probability` 0.0, `--xtc-threshold` 0.1.
- DRY: `--dry-multiplier` 0.0 (off), `--dry-base` 1.75, `--dry-allowed-length` 2, `--dry-penalty-last-n` 64 (0 disables), `--dry-sequence-breaker`.
- Mirostat: `--mirostat` 0 (off), 1, or 2; `--mirostat-lr` (eta) 0.1; `--mirostat-ent` (tau) 5.0.
- `--dynatemp-range` 0.0 and `--dynatemp-exp` 1.0 for dynamic temperature.
- `-l, --logit-bias TOKEN_ID(+/-)BIAS`; `--ignore-eos`.
- `--adaptive-target` and `--adaptive-decay` configure adaptive-p sampling.
- `-bs, --backend-sampling`: enable backend sampling (experimental, default disabled).

Many of these have matching `/completion` request fields (for example `temperature`, `top_k`, `top_p`, `min_p`, `repeat_penalty`, `seed`, `mirostat`, `dry_multiplier` and `samplers`). The request fields document their own defaults, which can differ from the flag defaults above; the README lists `repeat_penalty` as 1.1 on the request.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: the default sampler order and sampler-seq, and the flag defaults listed above; /completion request fields and defaults. Corrected: the --dry-penalty-last-n default (64, not -1). Removed: the -1 meaning for --repeat-last-n and the server-wide-default versus per-request override sentence (not stated).

Method: docs-only read of cited pages, 2026-11-08
