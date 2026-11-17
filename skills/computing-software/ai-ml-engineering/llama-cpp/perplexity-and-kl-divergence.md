---
id: computing-software.ai-ml-engineering.llama-cpp.perplexity-and-kl-divergence
name: perplexity-and-kl-divergence
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, perplexity, kl-divergence, wikitext, quality-testing]
level: advanced
status: docs-checked
description: "Measure quantization quality with the llama.cpp perplexity tool, including the KL-divergence workflow against an FP16 baseline."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/perplexity/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Perplexity and KL divergence

The perplexity example measures how well a model predicts the next token over a text corpus; lower is better. It is not directly comparable between models, especially with different tokenizers, and finetunes typically have higher perplexity even when human-rated quality rises. Within llama.cpp it is used on base models to judge quality loss of quantized models versus FP16. The contributor convention is the Wikitext-2 test set (`scripts/get-wikitext-2.sh`), with default arguments and build options. llama.cpp numbers are not comparable to other projects'. By default only the mean perplexity and its uncertainty are computed.

**KL divergence** needs the FP16 logits recorded first:

1. Run perplexity on the FP16 model with `--kl-divergence-base path/to/file.kld`; it saves all logits in binary format. The file is very large: 11 GiB for LLaMA 2 or 37 GiB for LLaMA 3 on the Wikitext-2 test set.
2. Run perplexity with the quantized model, the same `--kl-divergence-base` file, and `--kl-divergence`. A KL divergence of 0 means the distributions are the same.

With `--kl-divergence` it also reports the PPL ratio and difference against FP16, mean change in the "correct" token probability (mean delta-p), the Pearson correlation of those probabilities, percentiles of the change, RMS delta-p, and same-top-p (how often both models assign the highest probability to the same token). Symmetric percentiles suggest quantization is only adding noise; clearly larger negative values suggest the model is getting worse.

The README's Llama 3 8B scoreboard (CUDA, sorted by KLD) lists `q6_K` at KLD 0.005452 and `q4_K_M` without imatrix at KLD 0.031273. The logits file stores FP16 logits cast to 16-bit unsigned integers, so the "f16" row is the difference from that downcast alone.

## Checked

2026-11-04: confirmed against the llama.cpp `tools/perplexity/README.md` page. Removed the shell commands (the page shows only the flags), the `-c`/`-b` and importance-matrix advice, and the delete-the-base-file tip, none of which the page states.
Method: documentation only; no commands were run.
