---
id: computing-software.ai-ml-engineering.llama-cpp.quantize-workflow
name: quantize-workflow
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, quantize, convert-hf-to-gguf, gguf, llama-quantize]
level: practitioner
status: docs-checked
description: "Convert a Hugging Face model to GGUF and quantize it with llama-quantize."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Convert and quantize

Quantization is two phases: convert the original model to GGUF, then quantize the GGUF. Install the Python requirements first (`python3 -m pip install -r requirements.txt`). Quantization can lose accuracy, usually measured in perplexity and/or KL divergence; a suitable imatrix file can minimize it.

1. Convert a Hugging Face model to a high-precision GGUF (the page uses `--remote` to pull from the hub):

```bash
python convert_hf_to_gguf.py --outfile gemma-4-E2B-it-bf16.gguf --outtype bf16 --remote google/gemma-4-E2B-it
```

If the model was downloaded locally, pass its directory and drop `--remote`. When the model is distributed in 16-bit format, `--outtype auto` (or omitting `--outtype`) also works well. The requirements install transformers 4, but newer models (such as Gemma 4) need transformers 5; the page says `pip install -U transformers` is safe.

2. Quantize:

```bash
./build/bin/llama-quantize gemma-4-E2B-it-bf16.gguf gemma-4-E2B-it-Q4_K_M.gguf Q4_K_M
```

The page's other examples append a thread count (for example `... q4_k_m 8`).

3. For multimodal models, convert the encoders and projectors separately to an `mmproj` GGUF with `convert_hf_to_gguf.py --mmproj`; keep it in a high-quality format such as bf16 or q8, because a smaller quant barely affects speed or memory but can hurt quality.

Quantizing already-quantized tensors needs `--allow-requantize` and can severely reduce quality, so start from a 16-bit or 32-bit source. Models are fully loaded into memory, so memory and disk requirements are the same; the page's Llama 3.1 example at Q4_K_M: 8B goes from 32.1 GB to 4.9 GB, 70B from 280.9 GB to 43.1 GB, 405B from 1,625.1 GB to 249.1 GB.

## Checked

2026-11-04: confirmed against the llama.cpp `tools/quantize/README.md` page (overview, conversion, quantize, multimodal and memory sections). Removed the `--outtype` value list beyond what the page shows, "no arguments lists types", the generic `llama-cli -p "Hello"` test and the closing paragraph.
Method: documentation only; no commands were run.
