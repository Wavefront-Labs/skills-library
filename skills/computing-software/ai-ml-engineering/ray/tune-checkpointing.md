---
id: computing-software.ai-ml-engineering.ray.tune-checkpointing
name: tune-checkpointing
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, tune-checkpoint, tune-callbacks, tune-stopper, tune-restore]
level: practitioner
status: docs-checked
description: "Checkpoint and resume Ray Tune trials with tune.report/get_checkpoint, add callbacks and stop criteria, and restore experiments with Tuner.restore."
sources:
  - https://docs.ray.io/en/latest/tune/tutorials/tune-trial-checkpoints.html
  - https://docs.ray.io/en/latest/tune/tutorials/tune-fault-tolerance.html
  - https://docs.ray.io/en/latest/tune/tutorials/tune-stopping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tune checkpointing

```python
import os, tempfile, torch
from ray import tune
from ray.tune import Checkpoint

def trainable(config):
    start = 1
    checkpoint = tune.get_checkpoint()                  # latest trial checkpoint when Tune restores the trial
    if checkpoint:
        with checkpoint.as_directory() as d:
            st = torch.load(os.path.join(d, "checkpoint.pt"))
            model.load_state_dict(st["model_state"]); start = st["epoch"] + 1
    for epoch in range(start, config["epochs"] + 1):
        ...                                             # train one epoch
        with tempfile.TemporaryDirectory() as d:
            torch.save({"epoch": epoch, "model_state": model.state_dict()},
                       os.path.join(d, "checkpoint.pt"))
            tune.report({"metric": 1}, checkpoint=Checkpoint.from_directory(d))

tuner = tune.Tuner(
    trainable, param_space={"epochs": 5},
    run_config=tune.RunConfig(
        storage_path="<STORAGE_URI>", name="exp",
        stop={"training_iteration": 5},
        failure_config=tune.FailureConfig(max_failures=3),
        checkpoint_config=tune.CheckpointConfig(num_to_keep=2),
        callbacks=[MyCallback()]))                      # MyCallback subclasses tune.Callback
tuner.fit()

tune.Tuner.restore("<STORAGE_URI>/exp", trainable=trainable, resume_errored=True).fit()
```

## Facts from the docs and API source
- Report each checkpoint together with metrics so Tune can order checkpoints. `tune.get_checkpoint()` returns the trial's latest checkpoint whenever Tune restores a trial (retry after failure, experiment restore, or resuming after a pause such as PBT).
- Function API: `checkpoint_frequency` and `checkpoint_at_end` do not work, so checkpoint manually (for example every N epochs). `num_to_keep`, `checkpoint_score_attribute` and `checkpoint_score_order` do work. Class API (`tune.Trainable` with `save_checkpoint`/`load_checkpoint`) supports all of them.
- `stop` can be a dict, a function or a `Stopper`. `FailureConfig(max_failures=3)` reschedules a failed trial (or trials on a failed node) up to 3 times; `fail_fast=True` stops the whole experiment on any error.
- `Tuner.restore(path, trainable, resume_unfinished=True, resume_errored=False, restart_errored=False, param_space=None)` resumes the exact job; `TERMINATED` trials cannot be resumed, and it cannot change search space or stopping criteria. Restoration cannot fix bugs; the cause must be ephemeral. `Tuner.can_restore(path)` supports a single launch-or-restore script. Re-specify `param_space` on restore when it contains object references.
- Multi-node runs need cloud or shared network storage via `storage_path`; saving trial checkpoints to the head node's local disk on a multi-node cluster raises an error. Restore from the cloud URI, not the head node's local directory.

## Verify
Interrupt the run, call `Tuner.restore`, and check that trials continue from their last checkpoint epoch.

## Checked
2026-11-03. Confirmed in Ray repo docs `tune/tutorials/tune-trial-checkpoints.md`, `tune-fault-tolerance.md`, `tune-stopping.md`, `tune-storage.md`, `doc_code/trial_checkpoint.py`, `fault_tolerance.py` and `python/ray/tune/tuner.py`. Fixed: the skill used `ray.train` (`train.report`, `train.RunConfig`) in Tune; current docs use `tune.report`, `tune.RunConfig`, `tune.Checkpoint`. Removed: "changing param_space is not supported" (restore accepts `param_space`), `results.get_dataframe()` check.
Method: documentation only; no commands were run.
