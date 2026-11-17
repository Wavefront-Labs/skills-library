---
id: computing-software.ai-ml-engineering.model-training.deterministic-training-resume
name: deterministic-training-resume
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, resume-determinism, checkpoint-resume, rng-state, data-order, statefuldataloader, reproducibility]
level: practitioner
status: draft
description: "Resume interrupted training so it continues exactly as an uninterrupted run would: saving RNG states, sampler and dataloader position, scheduler and scaler state, and verifying."
sources:
  - https://pytorch.org/docs/stable/notes/randomness.html
  - https://pytorch.org/data/beta/torchdata.stateful_dataloader.html
  - https://huggingface.co/docs/accelerate/usage_guides/checkpoint
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Deterministic resume (data order / RNG state)

A resumed run that "works" but sees a different data order or different dropout masks is not the same experiment: loss curves jump, and bitwise comparisons and debugging become impossible.

## Save everything that evolves
```python
state = {
    "model": model.state_dict(), "optimizer": opt.state_dict(), "scheduler": sched.state_dict(),
    "scaler": scaler.state_dict(), "step": step, "epoch": epoch,
    "rng": {"python": random.getstate(), "numpy": np.random.get_state(),
            "torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all()},
    "dataloader": loader.state_dict(),            # StatefulDataLoader
}
torch.save(state, path)
```
Restore all of them, in the same order, before the first post-resume step. Per-rank RNG state must be saved per rank in distributed training.

## Data order
- **Epoch boundary**: if the sampler shuffles with `generator` seeded by `base_seed + epoch` (DistributedSampler uses `set_epoch(epoch)`), resuming at an epoch start reproduces the order.
- **Mid-epoch**: either skip already-consumed batches (`accelerator.skip_first_batches(loader, n)`; costs time for data loading but is exact if order is deterministic) or use `torchdata.stateful_dataloader.StatefulDataLoader`, which saves sampler and worker iterator states (`loader.state_dict()` / `load_state_dict()`).
- Worker augmentation randomness: seed each worker from the base seed and worker id (`worker_init_fn`, or rely on PyTorch's default per-worker seeding derived from the base RNG, which is restored with the torch RNG state).
- Streaming datasets (WebDataset, HF streaming, Mosaic Streaming): use their resumable state APIs.

## Framework helpers
- Accelerate: `accelerator.save_state(dir)` / `load_state(dir)` saves model, optimizer, scheduler, scaler and RNG states; combine with `skip_first_batches`.
- HF Trainer: `trainer.train(resume_from_checkpoint=True)` restores RNG and skips batches (`ignore_data_skip=False`).
- Lightning: `trainer.fit(model, ckpt_path="last")` restores loops; mid-epoch exactness needs stateful loaders.

## Limits
Bitwise identity also needs deterministic kernels (`torch.use_deterministic_algorithms(True)`, `CUBLAS_WORKSPACE_CONFIG=:4096:8`), same hardware, same software versions and same world size. Changing GPU count on resume changes data sharding and reduction order: aim for statistical, not bitwise, equivalence then.

## Verify
Run N steps uninterrupted and log loss per step; run N/2, save, kill, resume, run N/2. Compare per-step losses: identical (deterministic setup) or within float noise. Any systematic jump at the resume step means some state was not restored.
