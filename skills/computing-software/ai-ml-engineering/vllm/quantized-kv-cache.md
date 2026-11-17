---
id: computing-software.ai-ml-engineering.vllm.quantized-kv-cache
name: quantized-kv-cache
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [kv-cache-dtype, fp8-kv-cache, kv-cache-dtype-skip-layers, calibration, per-attention-head]
level: practitioner
status: docs-checked
description: "Store the KV cache in FP8 with kv_cache_dtype, choose scale calibration, and skip sensitive layers."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shrink the KV cache to store more tokens and support longer contexts.

Enable with `kv_cache_dtype="fp8"` (or `--kv-cache-dtype fp8`). With the Flash Attention 3 backend, attention itself runs in FP8, so queries are also quantized.

Schemes:
- Per-tensor: one scale each for Q, K and V (`q/k/v_scale = [1]`).
- Per-attention-head: `q_scale = [num_heads]`, `k/v_scale = [num_kv_heads]`. Available only with the Flash Attention backend and requires llm-compressor calibration.

Scale calibration:
1. No calibration (default): all scales are `1.0`, via `kv_cache_dtype="fp8"`.
2. Recommended: calibrate with a dataset via llm-compressor (`pip install llmcompressor`). Its example uses `ultrachat_200k`, 512 samples, max length 2048, `STRATEGY = "tensor"` or `"attn_head"`, a `QuantizationModifier` with an `attention` config group targeting `LlamaAttention` for q_scale, and `kv_cache_scheme` set to FP8 `QuantizationArgs`.

Other dtype values:
- `auto`: the model's default dtype.
- `fp8_e4m3`: CUDA 11.8+ and ROCm.
- `fp8_e5m2`: CUDA 11.8+.

Sliding-window layers can be more sensitive. `--kv-cache-dtype-skip-layers` leaves chosen layers at the native dtype, by type name or index:

```bash
vllm serve <model> --kv-cache-dtype fp8 --kv-cache-dtype-skip-layers sliding_window
vllm serve <model> --kv-cache-dtype fp8 --kv-cache-dtype-skip-layers 0 1 23
```

Python: `LLM(model=..., kv_cache_dtype="fp8", kv_cache_dtype_skip_layers=["sliding_window"])`.

## Checked

2026-11-03. Confirmed against the Quantized KV Cache page (docs.vllm.ai/en/latest/): FP8 KV cache usage, scale schemes, calibration example, dtype support and skip-layers flag.

Method: documentation only; no commands were run.
