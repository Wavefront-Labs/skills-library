---
id: computing-software.ai-ml-engineering.pytorch.training-loop
name: training-loop
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch, training-loop, dataloader, num-workers, pin-memory, amp, mixed-precision, torch-autocast, gradscaler, bf16, gradient-clipping, clip-grad-norm, checkpointing, resume-training, lr-scheduler, torch-compile, ddp, distributed-data-parallel, torchrun, distributedsampler, model-train, model-eval, no-grad, deep-learning]
level: practitioner
status: gated
description: "Write a correct PyTorch training loop: train/eval modes, fast DataLoader, AMP (fp16 GradScaler or bf16), grad clipping, full checkpoint/resume, torch.compile and DDP via torchrun."
sources:
  - https://pytorch.org/docs/stable/index.html
  - https://pytorch.org/docs/stable/amp.html
  - https://pytorch.org/docs/stable/data.html
  - https://pytorch.org/tutorials/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PyTorch Training Loop — correct, fast, resumable

**Goal:** a loop that trains correctly (modes, gradients, precision), keeps the GPU busy, and can be killed and resumed without changing the result.

## 1. The skeleton
```python
model = Net().to(device)
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-4, total_steps=total_steps)
loss_fn = torch.nn.CrossEntropyLoss()

for epoch in range(start_epoch, epochs):
    model.train()
    for x, y in train_loader:
        x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            loss = loss_fn(model(x), y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        opt.step()
        sched.step()          # per-step scheduler; epoch schedulers go after the epoch
    evaluate(model, val_loader)
```
- `model.train()` / `model.eval()` switch dropout and BatchNorm behaviour. Forgetting `eval()` makes validation noisy and BatchNorm running stats drift.
- Wrap evaluation in `torch.no_grad()` (or `torch.inference_mode()`) — otherwise you store activations for a backward pass that never happens and run out of memory.
- `CrossEntropyLoss` expects raw logits, not softmax output. Applying softmax first is a silent accuracy killer.
- Order matters: `zero_grad → forward → backward → clip → step → scheduler.step`. Calling `sched.step()` before `opt.step()` triggers a warning and skips the first LR value.

## 2. Keep the GPU fed
- `DataLoader(ds, batch_size=..., shuffle=True, num_workers=N, pin_memory=True, persistent_workers=True, prefetch_factor=2)`. Start `num_workers` around the number of CPU cores per GPU (often 4–8) and tune by watching GPU utilisation.
- `pin_memory=True` plus `.to(device, non_blocking=True)` overlaps host-to-device copies.
- Gotcha (gated: unconfirmed, source is paywalled or blocked): with `num_workers>0`, each worker gets a copy of the dataset object; random augmentations seeded from NumPy can repeat across workers in older setups — use `worker_init_fn` or torch's own RNG.
- Gotcha: on macOS/Windows workers use spawn, so the dataset must be picklable and the entry point guarded with `if __name__ == "__main__":`.

## 3. Mixed precision
- **bf16** (Ampere and newer (gated: unconfirmed, source is paywalled or blocked)): `torch.autocast(device_type="cuda", dtype=torch.bfloat16)` and no scaler needed — same exponent range as fp32.
- **fp16** (older GPUs): needs loss scaling.
```python
scaler = torch.amp.GradScaler("cuda")
with torch.autocast("cuda", dtype=torch.float16):
    loss = loss_fn(model(x), y)
scaler.scale(loss).backward()
scaler.unscale_(opt)                       # must unscale BEFORE clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
scaler.step(opt); scaler.update()
```
The `torch.amp.GradScaler("cuda")` spelling is current; older code uses `torch.cuda.amp.GradScaler()`, which is deprecated in recent releases. Clipping scaled gradients without `unscale_` clips against the wrong norm.

## 4. Checkpoint and resume (everything, not just weights)
```python
torch.save({"model": model.state_dict(), "optim": opt.state_dict(),
            "sched": sched.state_dict(), "scaler": scaler.state_dict(),
            "epoch": epoch, "step": step,
            "rng": {"torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all()}},
           tmp_path)
os.replace(tmp_path, ckpt_path)            # atomic: a crash mid-save keeps the old file
```
- Resume: build model and optimizer first, then `load_state_dict` each, restore RNG states, continue from `epoch+1`. Restoring weights only resets Adam moments and the LR schedule — the run diverges or warms up again.
- Load with `torch.load(path, map_location=device)`. Recent PyTorch defaults `weights_only=True`; a dict with plain tensors and numbers loads fine, custom objects need allow-listing (check your version's docs).
- Save from rank 0 only in distributed runs; save `model.module.state_dict()` (DDP) or the original module (compiled) so keys do not carry `module.` / `_orig_mod.` prefixes.

## 5. torch.compile
`model = torch.compile(model)` (PyTorch 2.x) can speed up training (the gain depends on the model and hardware; measure it), but the first steps are slow while graphs compile, and dynamic shapes (variable sequence lengths) cause recompiles — pad to buckets or pass `dynamic=True`. Benchmark after warm-up, not on step 1.

## 6. DDP with torchrun
The DDP/NCCL/torchrun steps below were not run here (no GPU, no NCCL) (gated: unconfirmed, source is paywalled or blocked). The `find_unused_parameters` error was reproduced on gloo with world size 1.
```bash
torchrun --nproc_per_node=4 train.py
```
In the script: `torch.distributed.init_process_group("nccl")`, `local_rank = int(os.environ["LOCAL_RANK"])`, `torch.cuda.set_device(local_rank)`, wrap with `DistributedDataParallel(model, device_ids=[local_rank])`, use `DistributedSampler` and call `sampler.set_epoch(epoch)` each epoch (forget it and every epoch sees the same shuffle). Batch size is per process; the effective batch is `per_gpu × world_size`, so revisit the learning rate. Logging and checkpointing only on rank 0. For cluster sizing see computing-software.ai-ml-engineering.ml-platform-engineering.gpu-training-compute.

## Verify
- [ ] Validation runs under `model.eval()` and `torch.no_grad()`; val loss is identical across two runs on the same weights.
- [ ] A run killed at step N and resumed produces the same loss curve (within noise) as an uninterrupted run.
- [ ] The checkpoint contains model, optimizer, scheduler, scaler (if fp16), epoch/step and RNG state.
- [ ] GPU utilisation stays high (>80% for compute-bound models) after DataLoader tuning.
- [ ] With fp16, `scaler.unscale_` is called before clipping; no NaN losses in the first 1000 steps.
- [ ] Under DDP, `sampler.set_epoch` is called and only rank 0 writes files.
