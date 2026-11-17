---
id: computing-software.ai-ml-engineering.pytorch.half-precision-inference
name: half-precision-inference
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, half-precision-inference, bf16, fp16, inference, torch-dtype, inference-mode]
level: practitioner
status: verified
description: "Run inference in bf16/fp16 weights safely: casting the model vs autocast, keeping norms/softmax stable, batchnorm and output parity checks against fp32."
sources:
  - https://pytorch.org/docs/stable/amp.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.half
  - https://huggingface.co/docs/transformers/main/en/main_classes/model#model-instantiation-dtype
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Half-precision inference

**Goal:** halve memory and speed up inference by running weights and activations in bf16/fp16 while keeping outputs within tolerance of fp32.

## Two approaches
| Approach | How | When |
|---|---|---|
| Cast weights | `model = model.to(torch.bfloat16).eval()` and cast inputs | LLMs and transformers; max memory savings |
| Autocast with fp32 weights | `with torch.autocast(device, dtype=torch.float16): out = model(x)` (runs on `"cpu"` too on torch 2.14; weights stay fp32) | Legacy CNNs or models with sensitive layers; keeps fp32 master weights |

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device, dtype=torch.bfloat16).eval()
with torch.inference_mode():
    out = model(x.to(device, dtype=torch.bfloat16))
probs = out.float().softmax(-1)          # do final softmax/argmax decisions in fp32
```
Hugging Face: the model docs name the argument `dtype` (they describe it as overriding the older `torch_dtype`): `AutoModel.from_pretrained(name, dtype=torch.bfloat16)`, or `dtype="auto"` to use the dtype recorded in the checkpoint config, which the docs warn is the saved dtype, not necessarily the training dtype (docs page read; transformers not installed so not run).

## bf16 vs fp16
- bf16: fp32 range (max 3.39e38), 7 explicit mantissa bits (`finfo.eps` 7.8e-3, about 2 significant digits). Check hardware support with `torch.cuda.is_bf16_supported()`; bf16 `nn.Sequential` inference ran on a CPU build.
- fp16: more precision (`finfo.eps` 9.8e-4), small range (max 65504; `torch.tensor(70000.).half()` is `inf`). Models trained in bf16 can overflow when run in fp16, so test for `inf` and run those in bf16 or fp32.

## Keep stable
- LayerNorm/RMSNorm: compute variance in fp32 (most HF implementations upcast internally; check custom ones).
- Softmax/log-softmax over large vocabularies: upcast logits.
- BatchNorm in fp16 eval ran fine on CPU (max abs diff 3.7e-4 vs fp32 for a small conv net). `torch.nn.utils.fusion.fuse_conv_bn_eval(conv, bn)` fuses them (output differs by about 6e-7 in fp32); speed gain not measured here.
- Integer buffers (position ids) must stay integer; `model.half()` already leaves them alone (an int64 buffer and `num_batches_tracked` stayed int64; float buffers became fp16).

## Parity check before shipping
```python
ref = model_fp32(x)
cand = model_bf16(x.bfloat16()).float()
print((ref - cand).abs().max(), torch.nn.functional.cosine_similarity(ref.flatten(), cand.flatten(), dim=0))
```
For classifiers also compare top-1 agreement on a validation set (choose your own threshold; a tiny random CNN gave maxdiff 2.8e-3, cosine 0.999995 and 100% top-1 agreement in bf16); for LLMs compare perplexity on a held-out set.

## Verify
- [ ] Task metric within agreed tolerance of fp32 on a full validation set.
- [ ] No inf/NaN in outputs across the validation set.
- [ ] Measured latency and memory (not assumed) improved.
