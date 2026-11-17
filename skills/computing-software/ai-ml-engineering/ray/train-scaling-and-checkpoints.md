---
id: computing-software.ai-ml-engineering.ray.train-scaling-and-checkpoints
name: train-scaling-and-checkpoints
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, scaling-config, train-checkpoint, checkpoint-config, resume-from-checkpoint]
level: practitioner
status: docs-checked
description: "Configure Ray Train ScalingConfig and report/restore Checkpoints with CheckpointConfig, keep-best and resuming in the train loop."
sources:
  - https://docs.ray.io/en/latest/train/user-guides/checkpoints.html
  - https://docs.ray.io/en/latest/train/user-guides/fault-tolerance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ScalingConfig and checkpoints

```python
import os, tempfile, torch
import ray.train
from ray.train import ScalingConfig, CheckpointConfig, RunConfig, Checkpoint

scaling = ScalingConfig(num_workers=8, use_gpu=True,
                        resources_per_worker={"CPU": 4, "GPU": 1})
run = RunConfig(storage_path="<STORAGE_URI>", name="exp1",
    checkpoint_config=CheckpointConfig(num_to_keep=3,
        checkpoint_score_attribute="val_loss", checkpoint_score_order="min"))

def loop(config):
    start = 0
    ckpt = ray.train.get_checkpoint()                  # latest reported checkpoint on resume
    if ckpt:
        with ckpt.as_directory() as d:
            state = torch.load(os.path.join(d, "m.pt"))
            model.load_state_dict(state["model"]); start = state["epoch"] + 1
    for epoch in range(start, config["epochs"]):
        ...
        with tempfile.TemporaryDirectory() as d:
            ckpt = None
            if ray.train.get_context().get_world_rank() == 0:      # DDP: one copy is enough
                torch.save({"model": model.state_dict(), "epoch": epoch}, os.path.join(d, "m.pt"))
                ckpt = Checkpoint.from_directory(d)
            ray.train.report({"val_loss": v}, checkpoint=ckpt)     # call report on every rank
```

## Facts from the docs and API source
- `ScalingConfig`: `num_workers` (each worker reserves 1 CPU by default; in Train V2 it can also be a `(min, max)` tuple), `use_gpu` (1 GPU per worker), `resources_per_worker` (keys are case-sensitive: `CPU`, `GPU`, `TPU`, `memory`), `placement_strategy`, `accelerator_type` (experimental).
- Write the checkpoint to a local temp directory, then `ray.train.report(metrics, checkpoint=...)` uploads it to `storage_path`. The default upload is synchronous; an `ASYNC` mode needs the local directory kept alive until upload ends (use `tempfile.mkdtemp`, not `TemporaryDirectory`).
- In standard DDP every worker holds the full model, so save and report from one worker. With sharded strategies (DeepSpeed ZeRO, FSDP) each worker can report its shard; add a rank-specific suffix to file names to avoid collisions.
- `CheckpointConfig`: by default all checkpoints are kept; `num_to_keep` keeps the top K by `checkpoint_score_attribute` (`checkpoint_score_order` "max" default, or "min"), and the metric must be reported with the checkpoint. `result.best_checkpoints` lists them; `result.checkpoint` is the latest.
- After a failure restart, `get_checkpoint()` returns the latest reported checkpoint.

## Verify
`result.best_checkpoints` has at most `num_to_keep` entries; a rerun with the same `storage_path` and `name` resumes from the saved epoch.

## Checked
2026-11-03. Confirmed in Ray repo `train/user-guides/checkpoints.md`, `fault-tolerance.md` and `python/ray/train/v2/api/config.py`. Removed: `placement_strategy="PACK"` value (not checked against the placement-group page), "large checkpoints block the loop - save less often" advice, `TorchTrainer.restore` (deprecated, marked confirm), "omit it and the latest are kept" (the docs say all are kept).
Method: documentation only; no commands were run.
