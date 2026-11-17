---
id: computing-software.ai-ml-engineering.llama-cpp.quantize-tensor-options
name: quantize-tensor-options
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, llama-quantize, tensor-type, prune-layers, keep-split]
level: advanced
status: docs-checked
description: "Fine control over llama-quantize with per-tensor types, importance matrices, layer pruning and split output."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# llama-quantize options

The page's examples take the form `llama-quantize [options] input.gguf [output.gguf] type [threads]` (for example `... input-model-f32.gguf q4_k_m 8`).

- `--allow-requantize`: allow requantizing already-quantized tensors; can severely reduce quality versus quantizing from 16-bit or 32-bit.
- `--leave-output-tensor`: leave `output.weight` un(re)quantized; larger model, possibly better quality.
- `--pure`: disable k-quant mixtures and quantize all tensors to the same type.
- `--imatrix FILE`: use the file as an importance matrix.
- `--include-weights TENSOR`: use the imatrix for this tensor (repeatable). `--exclude-weights TENSOR`: use it for the tensors not specified. Include and exclude cannot be mixed.
- `--output-tensor-type TYPE`: quant type for `output.weight`.
- `--token-embedding-type TYPE`: quant type for the token embeddings tensor.
- `--keep-split`: produce the quantized model in the same shards as the input instead of a single file.
- Advanced: `--tensor-type` (specific tensors to specific types; regex syntax; repeatable), `--prune-layers` (remove the listed layers), `--override-kv` (override model metadata by key; repeatable).

Examples from the page:

```bash
# imatrix for specified tensors only
./llama-quantize --imatrix imatrix.gguf --include-weights attn_v --include-weights ffn_down input-model-f32.gguf q4_k_m 8

# set attn_v and ffn_down to Q5_K and prune layers 20, 21 and 22
./llama-quantize --imatrix imatrix.gguf --tensor-type attn_v=q5_k --tensor-type ffn_down=q5_k --prune-layers 20,21,22 input-model-f32.gguf q4_k_m 8

# copy tensors (no quantization), override metadata, prune layers, name the output
./llama-quantize --imatrix imatrix.gguf --override-kv qwen3moe.expert_used_count=int:16 --prune-layers 20,21,22 input-model-f32.gguf pruned-model-f32.gguf copy 8
```

## Checked

2026-11-04: confirmed against the llama.cpp `tools/quantize/README.md` page: all options and examples. Removed the `attn_v=q6_k` example, the `KEY=TYPE:VALUE` form (the page shows `key=int:16`), and the closing `--help` remark; the usage line is now presented as inferred from the page's examples.
Method: documentation only; no commands were run.
