---
id: computing-software.ai-ml-engineering.pytorch.gradient-accumulation-and-effective-batch-size
name: gradient-accumulation-and-effective-batch-size
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, gradient-accumulation-pytorch, effective-batch-size, loss-scaling, micro-batch, ddp-no-sync]
level: practitioner
status: verified
description: "Implement gradient accumulation in PyTorch with correct loss scaling, scheduler stepping, AMP, DDP no_sync and token-count normalisation for variable-length batches."
sources:
  - https://pytorch.org/docs/stable/notes/amp_examples.html#gradient-accumulation
  - https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html#torch.nn.parallel.DistributedDataParallel.no_sync
  - https://huggingface.co/blog/gradient_accumulation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gradient accumulation and effective batch size

Effective batch = micro_batch x accum_steps x world_size. Accumulate when the batch you want does not fit in memory.

## Correct loop (AMP + DDP)
```python
accum = 8
scaler = torch.amp.GradScaler("cuda")
opt.zero_grad(set_to_none=True)
for i, (x, y) in enumerate(loader):
    last = (i + 1) % accum == 0
    ctx = model.no_sync() if (ddp and not last) else contextlib.nullcontext()
    with ctx:
        with torch.autocast("cuda", dtype=torch.float16):
            loss = loss_fn(model(x), y) / accum          # scale so grads average
        scaler.scale(loss).backward()
    if last:
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt); scaler.update()
        opt.zero_grad(set_to_none=True)
        sched.step()                                     # once per optimizer step
```

## The details that go wrong
- **Divide the loss by accum**. Otherwise gradients are accum times larger, which effectively multiplies the LR (Adam is mostly scale-invariant, SGD is not, and clipping thresholds become wrong).
- **Token-level losses**: dividing each micro-batch's mean loss by accum weights short and long micro-batches equally, so it is not equal to the big-batch loss. Sum the per-token losses and divide by the total non-padding tokens across all micro-batches of the step (Hugging Face's "Fixing Gradient Accumulation" post, 16 Oct 2024, describes this bug and the fix in transformers).
- **Leftover micro-batches** at epoch end: either drop them or step with what accumulated; don't carry partial grads into the next epoch.
- **Scheduler and logging** count optimizer steps: total_steps = len(loader) // accum * epochs.
- **DDP**: without `no_sync`, every micro-batch triggers an all-reduce; accumulation then saves memory but not communication. FSDP1 has `no_sync` and FSDP2 uses `set_requires_gradient_sync(False)` (both exist in torch 2.14; only the API names were checked).
- **BatchNorm** sees only micro-batch statistics; accumulation doesn't fix small-batch BN. Use GroupNorm/LayerNorm or SyncBN.
- **Gradient checkpointing** is the other memory lever; accumulation keeps step math identical, checkpointing trades compute.

## Hyperparameters
Changing effective batch size changes optimal LR and warmup length (linear scaling for SGD and square-root scaling for Adam are common heuristics, not exact rules; tune). Keep the effective batch fixed when comparing hardware setups.

## Verify
On a small model, compare one step with batch 64 vs 8 x 8 accumulation (dropout off, same data order): gradients match within float tolerance (`torch.testing.assert_close` on `p.grad`; run here, it passes with the loss divided by `accum`, and without the division the gradient is 8x larger).

The loop above was run on a CPU-only host with `"cuda"` replaced by `"cpu"` (bf16 autocast, `GradScaler("cpu")`) and a one-process gloo `DDP`; 16 micro-batches with `accum = 8` gave exactly 2 optimizer and scheduler steps.
