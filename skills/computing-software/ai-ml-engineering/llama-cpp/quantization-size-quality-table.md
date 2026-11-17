---
id: computing-software.ai-ml-engineering.llama-cpp.quantization-size-quality-table
name: quantization-size-quality-table
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, quant-types, bits-per-weight, q4-k-m, model-size]
level: intro
status: docs-checked
description: "Reference sizes in GiB and bits per weight for common quantization types of an 8B model."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md", "https://github.com/ggml-org/llama.cpp/blob/master/tools/perplexity/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Quantization sizes

The quantize README tabulates meta-llama/Llama-3.1-8B across types. A few rows (bits per weight, size in GiB):

- `IQ1_S`: 2.0042 bpw, 1.87 GiB
- `Q2_K`: 3.1593 bpw, 2.95 GiB
- `Q4_K_M`: 4.8944 bpw, 4.58 GiB
- `Q6_K`: 6.5633 bpw, 6.14 GiB
- `Q8_0`: 8.5008 bpw, 7.95 GiB
- `F16`: 16.0005 bpw, 14.96 GiB

The same table lists prompt-processing and text-generation speeds per type, so the quantization choice trades disk size against inference speed.

Quality is measured in perplexity (PPL) and KL divergence (KLD). From the perplexity README's Llama 3 8B results (no importance matrix):

- `q6_K`: mean KLD 0.005452, PPL 6.253382
- `q4_K_M`: mean KLD 0.031273, PPL 6.407115
- `q2_K`: mean KLD 0.445132, PPL 9.751568

Multimodal components (mmproj) are usually kept in a high-quality format such as bf16 or q8.

## Checked

2026-11-04: confirmed against the llama.cpp quantize README (size and bits-per-weight table) and perplexity README (KLD and PPL table). Removed the size-equals-bits-times-parameters rule of thumb and the memory-bandwidth remark, the claim that IQ types benefit most from an imatrix, and the `--help` closing line; added the perplexity README as a source.
Method: documentation only; no commands were run.
