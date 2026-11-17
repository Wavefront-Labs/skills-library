---
id: computing-software.ai-ml-engineering.llama-cpp.imatrix-importance-matrix
name: imatrix-importance-matrix
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, imatrix, importance-matrix, calibration, quantization-quality]
level: advanced
status: docs-checked
description: "Compute and combine importance matrices with llama-imatrix to improve low-bit quantization."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/imatrix/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# llama-imatrix

`llama-imatrix` computes an importance matrix for a model and a text dataset; it can be used during quantization to improve the quality of the quantized model.

```bash
./llama-imatrix -m ggml-model-f16.gguf -f calibration-data.txt -ngl 99
./llama-quantize --imatrix imatrix.gguf ggml-model-f16.gguf ./ggml-model-q4_k_m.gguf q4_k_m
```

`-m` (model) and `-f` (calibration text file) are mandatory. Use `-ngl` for faster computation. Options:

- `-o, --output-file`: output file, default `imatrix.gguf`.
- `--output-format {gguf,dat}`: `dat` is the legacy format; default `gguf`. Per the page, saving to a file with an extension other than `.gguf` also writes the legacy format.
- `-ofreq, --output-frequency N`: save the result so far every N chunks (default 10).
- `--save-frequency N`: also save a separate copy every N chunks (default 0 = never).
- `--chunk N` (alias `--from-chunk`): skip the first N chunks. `--chunks N`: maximum chunks to process (default -1 = all).
- `--process-output`: also collect data for `output.weight` and `token_embd.weight` (when tied). Off by default because it is usually better not to use the imatrix for those tensors.
- `--no-ppl`: skip the perplexity calculation to go faster.
- `--parse-special`: parse special tokens such as `<|im_start|>`.
- `--in-file FILE` (repeatable): load existing imatrix files and combine them; also converts between formats.
- `--show-statistics`: display statistics of an imatrix file (use with `--in-file`).
- `--nextn`: collect data for MTP/NextN layers; needs a single sequence per batch (`--batch-size` <= `--ctx-size`) and cannot be used where NextN layers share the trunk's KV cache. `-md, --model-draft FNAME` supplies an external NextN draft file when the model lacks NextN layers.
- `-lv` sets verbosity (default 1).

Combine or convert:

```bash
./llama-imatrix --in-file imatrix-prev-0.gguf --in-file imatrix-prev-1.gguf -o imatrix-combined.gguf
./llama-imatrix --in-file imatrix-new-format.gguf --output-format dat -o imatrix-legacy-format.dat
```

## Checked

2026-11-04: confirmed against the llama.cpp `tools/imatrix/README.md` page: usage, every option above, defaults and examples. Fixed `--chunk` wording, `--process-output` scope and `--save-frequency`; removed the `--in-file` "(or convert)" ambiguity by using the page's conversion example, and the `build/bin` paths.
Method: documentation only; no commands were run.
