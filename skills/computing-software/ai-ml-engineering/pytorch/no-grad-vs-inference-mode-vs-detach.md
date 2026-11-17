---
id: computing-software.ai-ml-engineering.pytorch.no-grad-vs-inference-mode-vs-detach
name: no-grad-vs-inference-mode-vs-detach
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, inference-mode, no-grad, detach, enable-grad, evaluation]
level: practitioner
status: verified
description: "Choose correctly between torch.no_grad, torch.inference_mode, detach and requires_grad_(False) for evaluation, serving and partial graphs, and avoid inference-tensor errors."
sources:
  - https://pytorch.org/docs/stable/notes/autograd.html#locally-disabling-gradient-computation
  - https://pytorch.org/docs/stable/generated/torch.autograd.grad_mode.inference_mode.html
  - https://pytorch.org/docs/stable/generated/torch.Tensor.detach.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# no_grad vs inference_mode vs detach

## What each does
| Tool | Scope | Effect |
|---|---|---|
| `torch.no_grad()` | block / decorator | ops don't record graph; outputs have `requires_grad=False` but are normal tensors |
| `torch.inference_mode()` | block / decorator | like no_grad plus no version counters or view tracking; faster, but outputs are "inference tensors" |
| `t.detach()` | one tensor | new tensor sharing storage, cut from the graph |
| `p.requires_grad_(False)` | parameters | stop computing grads for these params (freezing) |
| `model.eval()` | module flag | changes dropout/batchnorm behaviour; has nothing to do with gradients |

`model.eval()` and `no_grad`/`inference_mode` are independent: evaluation needs both.

## Pick one
- Serving / offline batch prediction: `@torch.inference_mode()` on the predict function. Skips version counters and view tracking, so it can be faster than `no_grad` (the size of the gain is workload dependent; measure it).
- Validation inside a training loop: `torch.no_grad()` is the safe default; if any output might later be used in autograd (e.g. cached teacher logits mixed into a loss), inference_mode will bite.
- Target networks, teacher logits, EMA targets inside a training step: `with torch.no_grad(): t = teacher(x)` or `teacher(x).detach()`.
- Logging: `loss.detach()` or `loss.item()`; never append `loss` itself.

## Inference-tensor errors
Tensors created under `inference_mode` cannot later be saved for backward or modified in place outside it:
`RuntimeError: Inference tensors cannot be saved for backward. Please do not use Tensors created in inference mode in computation tracked by autograd. To work around this, you can make a clone to get a normal tensor ...` (run here: even using such a tensor as the input of `nn.Linear` followed by `backward()` raises it).
Fixes: use `no_grad` for that code path, or `t.clone()` outside inference mode. Common trigger: a cache (embeddings, KV, normalisation stats) filled under inference_mode then reused in training.

## Re-enabling inside a disabled block
`with torch.enable_grad():` inside `no_grad` turns tracking back on (useful for gradient-based attribution or test-time adaptation in an eval function). Inside `inference_mode` it does not help: run on torch 2.14, ops under `enable_grad` nested in `inference_mode` still returned `requires_grad=False` inference tensors.

## Detach gotchas
- `detach()` shares memory: an in-place op on the detached tensor changes the original and can trip autograd's version check.
- `x.detach().requires_grad_()` makes a new leaf; common for adversarial examples and input optimisation.
- `.data` is the legacy equivalent but skips version tracking; prefer `detach()`.

## Verify
`assert not out.requires_grad` after eval code; measure peak memory with `torch.cuda.max_memory_allocated()` with and without the context to confirm activations aren't being kept.
