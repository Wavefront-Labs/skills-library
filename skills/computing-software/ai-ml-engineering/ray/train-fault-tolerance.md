---
id: computing-software.ai-ml-engineering.ray.train-fault-tolerance
name: train-fault-tolerance
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, failure-config, max-failures, train-restore, elastic-training]
level: practitioner
status: docs-checked
description: "Make Ray Train jobs survive worker and node failures with FailureConfig(max_failures), checkpoint resume and rerunning with the same storage_path and name."
sources:
  - https://docs.ray.io/en/latest/train/user-guides/fault-tolerance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Train fault tolerance

```python
import tempfile, uuid
import ray.train
import ray.train.torch

def train_fn_per_worker(config):
    checkpoint = ray.train.get_checkpoint()            # latest reported checkpoint, if any
    if checkpoint:
        with checkpoint.as_directory() as d:
            ...                                        # load model/optimizer state
    with tempfile.TemporaryDirectory() as d:
        ...                                            # save state into d
        ray.train.report({"loss": 0.1}, checkpoint=ray.train.Checkpoint.from_directory(d))

trainer = ray.train.torch.TorchTrainer(
    train_fn_per_worker,
    scaling_config=ray.train.ScalingConfig(num_workers=4),
    run_config=ray.train.RunConfig(
        storage_path="<STORAGE_URI>",                  # shared storage when multi-node
        name=f"train_run-{uuid.uuid4().hex}",          # unique per run
        failure_config=ray.train.FailureConfig(max_failures=3)))   # -1 = no limit
trainer.fit()
```

## Facts from the docs
- Three levels: worker process failures, worker node failures, and job driver failures.
- On a worker or node failure Ray Train shuts down all workers, adds nodes if needed and starts a new set that resume from the latest checkpoint. Each recovery counts as a retry against `FailureConfig.max_failures`; the default 0 disables worker fault tolerance and -1 is unlimited.
- Progress is only kept if the training function saves checkpoints (via `ray.train.report`) and loads them via `ray.train.get_checkpoint()`; otherwise training restarts from scratch.
- Driver recovery: relaunch the same script with the same `RunConfig(storage_path, name)`; Ray Train reads run state from `{storage_path}/{name}`. A different pair starts a new run; reusing a name by accident resumes the old run, so pass a unique name per new run. Driver crashes do not count toward `max_failures`.
- Preemption has a separate budget, `FailureConfig(max_preemption_failures)`, default -1 (unlimited); exhausting it raises `PreemptionError`. The guide also covers saving a just-in-time checkpoint before preemption.
- `<Framework>Trainer.restore` and `can_restore` are deprecated as of Ray 2.43. Migrate by constructing the trainer normally with the same `storage_path` and `name` (Ray 2.50 or earlier needs `RAY_TRAIN_V2_ENABLED=1`). `Trainer(resume_from_checkpoint=...)` is also deprecated; pass the initial checkpoint through `train_loop_config`.

## Verify
Stop a worker node mid-run; the workers restart and `ray.train.get_checkpoint()` returns the last reported checkpoint.

## Checked
2026-11-03. Confirmed in Ray repo `doc/source/train/user-guides/fault-tolerance.md`, `doc_code/fault_tolerance.py` and `FailureConfig` in `python/ray/train/v2/api/config.py`. Fixed: `TorchTrainer.can_restore`/`restore` shown as the recovery path are deprecated. Removed: `CheckpointConfig` import omission example, spot/autoscaler advice, "unhandled exception counts" claim, `ray kill` verification.
Method: documentation only; no commands were run.
