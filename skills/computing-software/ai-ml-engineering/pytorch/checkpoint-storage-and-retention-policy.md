---
id: computing-software.ai-ml-engineering.pytorch.checkpoint-storage-and-retention-policy
name: checkpoint-storage-and-retention-policy
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, checkpoint-retention, checkpointing, object-storage, s3, fault-tolerance, training-resume]
level: practitioner
status: gated
description: "Store PyTorch training checkpoints on object storage with atomic writes, keep-last-N and best-K retention, manifests, and resume logic that survives preemption."
sources:
  - https://pytorch.org/docs/stable/distributed.checkpoint.html
  - https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Checkpoint storage to object stores and retention

## What a checkpoint holds
Model state, optimizer state, LR scheduler, GradScaler, step/epoch, RNG states (`random.getstate`, `numpy.random.get_state`, `torch.get_rng_state`, `torch.cuda.get_rng_state` per rank), dataloader/sampler state, and config + code version. Missing any of these makes resume diverge.

## Write pattern
1. Write locally (fast NVMe) or with DCP directly to storage, to a **temporary name**: `step_012000.tmp/`.
2. Finish all ranks (`dist.barrier()`), write a small `manifest.json` (step, metrics, files, sha256) last.
3. "Commit" by writing the manifest or a `latest` pointer file. Do not rely on an atomic rename on object stores (a rename there is a copy plus delete); the manifest is what marks a checkpoint complete. Readers ignore directories without a manifest.
4. Upload asynchronously so training continues: `torch.distributed.checkpoint.async_save` or a background thread copying the finished local directory (`aws s3 sync`, `gsutil -m rsync`, `s5cmd`; none of these CLIs was run here, no cloud account (gated: unconfirmed, source is paywalled or blocked)).

## Retention
- **Keep last N** (e.g. 3) for resume plus **best K** by validation metric plus **milestones** (every 10k steps) for analysis.
- Delete only after the newer checkpoint's manifest exists and upload is verified.
- Push long-term milestones to a cheaper class with lifecycle rules (S3 Lifecycle transitions, e.g. to S3 Glacier Flexible Retrieval, listed in the AWS lifecycle docs; GCS Nearline has a 30-day minimum storage duration per the storage-classes page) rather than deleting from code. Any "after 30 days" threshold is your policy choice, not a platform default.
- Lightning 2.6.6: `ModelCheckpoint(dirpath="s3://bucket/run/", save_top_k=3, monitor="val/loss", save_last=True, every_n_train_steps=1000)` accepts all five arguments, but constructing it with an `s3://` path raised `ImportError: Install s3fs to access S3` until `s3fs` is installed.

## Frequency
Pick interval so expected lost work is acceptable: with preemption rate p per hour and checkpoint cost c, saving every ~sqrt(2c / p) hours is near optimal (Young's first-order formula, interval = sqrt(2 x cost x mean time between failures); with c = 30 s and one preemption a day it gives 0.63 h). Spot/preemptible jobs: also checkpoint on the termination signal (Google Compute Engine's Spot shutdown period is best effort and up to 30 seconds, and the preemption notice can be configured up to 120 seconds; AWS issues a two-minute Spot interruption notice). Whether the signal is SIGTERM depends on your OS and VM setup (not run).

## Resume logic
```python
def latest_complete(prefix):
    mans = sorted(list_objects(prefix, suffix="manifest.json"))
    return mans[-1] if mans else None
```
On start: find latest manifest, load it, verify step and config hash match, restore every state. Log "resumed from step N" loudly.

## Sizing
Adam checkpoint is ~3x fp32 model size (weights + two moments) plus any master copies. A 7B-parameter model is 7e9 x 4 B x 3 = 84 GB (78 GiB) per full checkpoint; sharded DCP writes in parallel from every rank, which is the main lever for save time.

## Gotchas
- Saving only on rank 0 with FSDP gathers the full model to one GPU/CPU and can OOM (reasoned, not measured); use DCP sharded save (which wrote one data file per rank in a 2-rank run).
- Network filesystems with eventual consistency: verify file sizes or checksums before deleting older checkpoints.
- Version the checkpoint format; renamed modules break old checkpoints silently with `strict=False`.
