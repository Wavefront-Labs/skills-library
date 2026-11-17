---
id: computing-software.ai-ml-engineering.hugging-face.gguf-conversion-llama-cpp
name: gguf-conversion-llama-cpp
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, gguf, llama-cpp, quantization, local-inference, k-quants]
level: practitioner
status: docs-checked
description: "Convert Hugging Face models to GGUF and quantize with llama.cpp: convert_hf_to_gguf, llama-quantize types (Q4_K_M, Q8_0), imatrix, GGUF-my-repo and the Hub GGUF viewer."
sources:
  - https://github.com/ggml-org/llama.cpp
  - https://huggingface.co/docs/hub/gguf
  - https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GGUF conversion and llama.cpp quantization

**Use for:** local inference with llama.cpp and other GGUF-capable runtimes.

## Convert
```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
python convert_hf_to_gguf.py <hf_model_dir> --outfile model-bf16.gguf --outtype bf16   # or q8_0
```
The README example uses `--outtype bf16`; for models already distributed in 16-bit, `--outtype auto` (or omitting it) also works well. Follow the llama.cpp README for installing requirements and building the binaries.

## Quantize
```bash
./build/bin/llama-quantize --imatrix imatrix.dat model-bf16.gguf model-Q4_K_M.gguf Q4_K_M   # --imatrix is optional
```
Quantization may lose accuracy (measured as perplexity or KL divergence); a suitable importance-matrix (imatrix) file can minimise that.
| Type | Bits/weight (measured on the README's example model) |
|---|---|
| Q8_0 | 8.50 |
| Q6_K | 6.56 |
| Q5_K_M | 5.70 |
| Q4_K_M | 4.89 |
| IQ3_XXS | 3.25 |
| Q2_K | 3.16 |
Exact figures vary by model; the README table also lists sizes and speeds.

## Multimodal
The README says multimodal projector components are usually kept in a high-quality format such as bf16 or q8, because a smaller quant saves little speed or memory and can hurt quality.

## Hub
The Hub has a GGUF viewer showing metadata and tensor info (name, shape, precision), and the `ggml-org/gguf-my-repo` tool converts and quantizes weights to GGUF.

## Verify
- [ ] Compare perplexity (or KL divergence) against the unquantized GGUF on the same text.
- [ ] Task-level spot check on your own prompts.

## Checked
2026-11-01. Confirmed against the llama.cpp quantize README and the Hugging Face Hub GGUF page: `convert_hf_to_gguf.py` with `--outtype bf16`/`q8_0`/`auto`, `llama-quantize --imatrix`, bits/weight for Q8_0, Q6_K, Q5_K_M, Q4_K_M, IQ3_XXS and Q2_K (Q4_K_M corrected from 4.8 to 4.89; IQ3_XXS/Q2_K from "2-3" to about 3.2), GGUF-my-repo, Hub GGUF viewer, multimodal guidance. Removed (not on the pages read): cmake and requirements steps, `llama-imatrix`, `convert_lora_to_gguf.py`, `llama-cli`/`llama-perplexity`/`llama-server` commands, Ollama Modelfile, chat-template note, perplexity-delta threshold.
Method: documentation only; no commands were run.
