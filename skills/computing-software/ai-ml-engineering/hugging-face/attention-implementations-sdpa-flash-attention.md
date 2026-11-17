---
id: computing-software.ai-ml-engineering.hugging-face.attention-implementations-sdpa-flash-attention
name: attention-implementations-sdpa-flash-attention
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, attn-implementation, flash-attention, sdpa, flex-attention, transformers, padding-free]
level: practitioner
status: gated
description: "Pick the Transformers attention backend: attn_implementation eager/sdpa/flash_attention_2/flex, install and dtype requirements, padding-free packing and debugging mismatches."
sources:
  - https://huggingface.co/docs/transformers/main/en/attention_interface
  - https://huggingface.co/docs/transformers/main/en/perf_infer_gpu_one
  - https://github.com/Dao-AILab/flash-attention
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Attention implementations (sdpa, flash_attention_2)

## Options
| `attn_implementation` | What | Requirements |
|---|---|---|
| `"sdpa"` (default when supported; `config._attn_implementation == "sdpa"` on a fresh load, ran) | `torch.nn.functional.scaled_dot_product_attention`, picks the fastest kernel on CUDA and the C++ implementation on other backends (docs) | PyTorch 2.x |
| `"flash_attention_2"` | Dao FlashAttention-2 kernels; supports unpadded (varlen) batches | `pip install flash-attn --no-build-isolation`, Ampere+ GPU, fp16/bf16 (gated: unconfirmed, source is paywalled or blocked). Without the package, loading raised `ImportError: FlashAttention2 has been toggled on, but it cannot be used`; the attention_interface docs say requesting FlashAttention by name falls back to a Hub kernel when one is available |
| `"flash_attention_3"` / kernels from the Hub (e.g. `"kernels-community/flash-attn2"`) | FA3 overlaps operations and fuses forward/backward more tightly (docs); Hopper-class GPUs (gated: unconfirmed, source is paywalled or blocked) |
| `"flex_attention"` | PyTorch FlexAttention for custom attention patterns (loaded fine on CPU torch 2.14.1; kernels not exercised) | recent PyTorch, compile |
| `"eager"` | plain matmul + softmax; returns attention weights | always works; slowest, most memory |

```python
model = AutoModelForCausalLM.from_pretrained(name, dtype=torch.bfloat16,    # torch_dtype= warns "deprecated" on 5.20.2
                                             attn_implementation="flash_attention_2", device_map="auto")
print(model.config._attn_implementation)
model.set_attn_implementation("sdpa")      # switch backend after loading (attention_interface docs)
```

## When it matters
- Long sequences: flash/SDPA kernels avoid the O(L^2) attention matrix in memory; enables long-context fine-tuning.
- Training with padding: FA2 + padding-free collation (`DataCollatorWithFlattening`, or TRL `padding_free=True`) packs sequences without cross-contamination, eliminating pad compute. `DataCollatorWithFlattening` ran: two rows `[1,2,3]` and `[4,5]` became one row with `position_ids [0,1,2,0,1]` and labels -100 at each sequence start. Only FlashAttention honours those position ids as sequence boundaries (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- FA2 in fp32 raises an error: load in bf16/fp16 (gated: unconfirmed, source is paywalled or blocked).
- `output_attentions=True` needs `eager`: on 5.20.2 a forward with `sdpa` returned an empty attentions tuple (length 0, no error) while `eager` returned one tensor per layer (2 for the tiny model), so a silent empty result is the symptom.
- Small numeric differences across implementations are normal; large ones usually mean a mask/position-id issue (check left padding and `position_ids`).
- Some architectures do not support every backend; Transformers raises at load time.
- Custom attention masks (non-causal, sliding window variants) may force the math kernel in SDPA, losing the speedup.

## Verify
- [ ] Compare logits between `eager` and the chosen implementation on the same batch. Measured on a tiny Llama, CPU: fp32 max abs diff 6e-8, bf16 max abs diff 2e-3 (eager vs sdpa); treat much larger gaps as a mask or position-id problem.
- [ ] Measure tokens/s and peak memory with each option at your sequence length.
