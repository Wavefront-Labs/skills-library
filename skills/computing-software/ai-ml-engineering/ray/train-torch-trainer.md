---
id: computing-software.ai-ml-engineering.ray.train-torch-trainer
name: train-torch-trainer
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, torch-trainer, ray-train, train-loop-per-worker, prepare-model]
level: practitioner
status: docs-checked
description: "Distributed PyTorch training with Ray Train TorchTrainer: train loop, prepare_model, prepare_data_loader, ScalingConfig and the Result."
sources:
  - https://docs.ray.io/en/latest/train/getting-started-pytorch.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TorchTrainer

```python
import os, tempfile, torch
import ray.train, ray.train.torch
from torch.utils.data import DataLoader

def train_func():
    model = ray.train.torch.prepare_model(MyNet())          # moves to device and wraps in DDP
    loader = DataLoader(dataset, batch_size=64, shuffle=True)   # batch_size is per worker
    loader = ray.train.torch.prepare_data_loader(loader)    # adds DistributedSampler, moves batches
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
    for epoch in range(5):
        if ray.train.get_context().get_world_size() > 1:
            loader.sampler.set_epoch(epoch)
        for x, y in loader:
            loss = torch.nn.functional.cross_entropy(model(x), y)
            opt.zero_grad(); loss.backward(); opt.step()
        with tempfile.TemporaryDirectory() as d:
            torch.save(model.module.state_dict(), os.path.join(d, "model.pt"))
            ray.train.report({"loss": loss.item()},
                             checkpoint=ray.train.Checkpoint.from_directory(d))

trainer = ray.train.torch.TorchTrainer(
    train_func,
    scaling_config=ray.train.ScalingConfig(num_workers=2, use_gpu=True),
    # multi-node: run_config=ray.train.RunConfig(storage_path="<STORAGE_URI>") on shared storage
)
result = trainer.fit()
with result.checkpoint.as_directory() as d:
    state = torch.load(os.path.join(d, "model.pt"))
```

## Facts from the docs
- `ScalingConfig` sets the worker count and GPU use; `TorchTrainer` launches the job.
- `prepare_model` moves the model to the right device and wraps it in `DistributedDataParallel`; hence `model.module.state_dict()` when saving.
- `prepare_data_loader` adds a `DistributedSampler` and moves batches to the device; it keeps an existing `DistributedSampler`'s configuration. Skip it if you feed a Ray Data dataset. `DataLoader`'s `batch_size` is per worker: global = worker batch size times `ray.train.get_context().get_world_size()`.
- Multi-node runs need `RunConfig(storage_path=...)` accessible from all nodes.
- Metrics passed to `ray.train.report` are attached to the checkpoint and used to decide which checkpoints to keep; for fault tolerance see the train-fault-tolerance skill.

## Verify
`result.metrics` and `result.checkpoint` are populated after `fit()`.

## Checked
2026-11-03. Confirmed in Ray repo `train/getting-started-pytorch.md` and `user-guides/checkpoints.md`. Removed: `train_loop_config` usage, "all workers must call report the same number of times" hang claim, NCCL seed advice, S3/NFS-only claim, `ray status` check, V2 "confirm" remark. Added `set_epoch` world-size guard as in the guide.
Method: documentation only; no commands were run.
