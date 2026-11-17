---
id: computing-software.ai-ml-engineering.vllm.online-quantization
name: online-quantization
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [online-quantization, fp8-per-tensor, fp8-per-block, mxfp8, mxfp4, quantization-config]
level: practitioner
status: docs-checked
description: "Quantize a BF16/FP16 model at load time with fp8_per_tensor, fp8_per_block, mxfp8 or mxfp4 and a quantization_config."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/online/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: quantize Linear and MoE weights to lower precision when the model loads, with no pre-quantized checkpoint or calibration data. Activations are scaled dynamically on every forward pass.

```python
llm = LLM("meta-llama/Llama-3.1-8B", quantization="fp8_per_tensor")
```

CLI: `vllm serve meta-llama/Llama-3.1-8B --quantization fp8_per_block`.

Schemes:
- `fp8_per_tensor`: fp8_e4m3 with an fp32 per-tensor scale; on Ada and Hopper linear activations may use per-token scaling.
- `fp8_per_block`: weights with fp32 per-128x128-block scale, activations per-1x128-block.
- `mxfp8`: e8m0 per-1x32-block scales; w8a8 needs SM 100+ (Blackwell or newer), other GPUs use a w8a16 fallback.
- `mxfp4`: fp4_e2m1 weights, e8m0 per-1x32 scales; the linear backend is auto-selected per platform (pin one with `--linear-backend`, e.g. `flashinfer`).

Fine-grained control uses a `quantization_config` dict:

```yaml
quantization_config:
  linear: {weight: <name>, activation: <name>}
  moe:    {weight: <name>, activation: <name>}
  ignore: [<layer-name-or-regex-or-fnmatch-pattern>]
```

Other schemes in the table: `lut_b_moe` (MoE only, native on Rubin SM 10.7, other GPUs emulate it; dense layers stay unquantized) and `mxfp4_hadamard32` (linear only; rotates weights and activations by a 32-wide Hadamard matrix before MXFP4 quantization).

`linear` and `moe` accept a `{weight, activation}` dict or a bare string. Unset fields fall back to the `--quantization` shorthand defaults. An explicit `activation: null` requests unquantized BF16 activations, which differs from omitting it. For online quantization only MXFP4 layers accept an activation override; other online weight formats reject it.

CLI forms: JSON, e.g. `--quantization-config '{"moe":{"activation":"mxfp8"}}'`, or dotted keys such as `--quantization-config.moe.activation mxfp8` (for pre-quantized gpt-oss MXFP4 MoE checkpoints, FP8 activations). Combine with `--moe-backend` to pin a kernel family.

Excluding layers: `ignore` takes exact names, `re:` regexes and fnmatch patterns. `targets` maps layer patterns to shorthands (`fp8_per_tensor`, `fp8_per_block`, `fp8_per_channel`, `mxfp8`, `mxfp4`, `mxfp4_hadamard32`, `int8_per_channel_weight_only`, `nvfp4_per_token`) or a `{weight, activation}` spec. `targets` is mutually exclusive with online `linear` and `moe`; unmatched layers keep their checkpoint dtype; a layer matching both `targets` and `ignore`, or two `targets` patterns, raises an error.

Re-quantizing a checkpoint at load is supported for ModelOpt MXFP8 linears and compressed-tensors, ModelOpt and Quark NVFP4 MoE layers. Example: `--quantization-config '{"targets":{"*mlp.experts*":"mxfp4"}}'`. Unsupported source/target pairs raise an error.

## Checked

Method: 2026-11-08 read the online quantization page in full. Scheme list, config schema and re-quantization claims matched. Replaced a misleading CLI example, and added lut_b_moe, hadamard, activation-override rules, ignore and targets.
