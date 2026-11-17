---
id: computing-software.ai-ml-engineering.pytorch.multiheadattention-and-attention-masks
name: multiheadattention-and-attention-masks
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, multiheadattention, attention-masks, transformerencoder, key-padding-mask, scaled-dot-product-attention, causal-mask]
level: practitioner
status: verified
description: "Use nn.MultiheadAttention and TransformerEncoder correctly: batch_first, key_padding_mask vs attn_mask semantics, causal masks, NaN rows and the fast path."
sources:
  - https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
  - https://pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html
  - https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nn.MultiheadAttention, TransformerEncoder and masks

**Goal:** get attention masks right first time; most transformer bugs are mask bugs.

## Shapes
- Use `batch_first=True` so inputs are `(B, L, E)`; the default is `(L, B, E)`.
- `embed_dim` must be divisible by `num_heads`.

## Two masks, different meanings
| Argument | Shape | Meaning of `True` (bool) |
|---|---|---|
| `key_padding_mask` | `(B, S)` | this key position is padding; ignore it |
| `attn_mask` | `(L, S)` or `(B*num_heads, L, S)` | this query may NOT attend to this key |

Float masks are added to the scores (use `-inf` to block, `0` to allow). Bool and float semantics are opposite to `F.scaled_dot_product_attention`, where a bool `True` means **allowed**. Converting code between them is a top source of silent bugs.

```python
import torch, torch.nn as nn
layer = nn.TransformerEncoderLayer(d_model=512, nhead=8, batch_first=True, norm_first=True)
enc = nn.TransformerEncoder(layer, num_layers=6, enable_nested_tensor=False)
pad = tokens.eq(pad_id)                                           # (B, S) True = pad
causal = torch.triu(torch.ones(S, S, dtype=torch.bool, device=x.device), 1)  # bool, True = blocked; same type as pad
out = enc(x, mask=causal, src_key_padding_mask=pad, is_causal=True)
```
`is_causal=True` is a hint that `mask` is causal; you must still pass the mask. Use the same mask type (both bool or both float) for the mask and the padding mask: mixing them (bool padding with the float mask from `generate_square_subsequent_mask`) emits a deprecation warning in torch 2.14.

## NaN outputs
A query row whose keys are all masked gives softmax over all `-inf` = NaN. Confirmed on torch 2.14: `nn.MultiheadAttention` returns NaN for a fully padded sequence, and for a left-padded batch with a causal mask the first padded query positions are NaN. Fix: ensure every query sees at least one key (e.g. do not mask the token itself), or zero those rows after attention.

## Performance
- The `nn.MultiheadAttention` inference fast path needs self-attention, batched `batch_first=True` input, no grad (`no_grad`/`inference_mode` or no `requires_grad` input), `.eval()`, no `add_bias_kv`/`add_zero_attn`, `kdim == vdim == embed_dim`, and autocast off (from the class docstring); it can then take nested tensors for padding.
- For custom blocks call `F.scaled_dot_product_attention(q, k, v, attn_mask=None, is_causal=True)` directly; with a bool `attn_mask` a lower-triangular `True` matrix (True = allowed) gives the same output as `is_causal=True` (checked). Prefer `is_causal` when no padding mask is needed so the backend can skip building a mask.
- `need_weights=True` is the default for MHA and returns head-averaged attention weights `(B, L, S)`; set `need_weights=False` when you do not read attention maps.

## Verify
- [ ] Changing padded token values does not change outputs at real positions.
- [ ] For causal models, perturbing token t+1 does not change output at t.
- [ ] `torch.isnan(out).any()` is False on a batch with heavy padding.
