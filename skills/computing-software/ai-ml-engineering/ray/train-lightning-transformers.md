---
id: computing-software.ai-ml-engineering.ray.train-lightning-transformers
name: train-lightning-transformers
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-train-lightning, hf-transformers, prepare-trainer, rayddpstrategy]
level: practitioner
status: docs-checked
description: "Run PyTorch Lightning and Hugging Face Transformers training under Ray Train with RayDDPStrategy, RayTrainReportCallback and prepare_trainer."
sources:
  - https://docs.ray.io/en/latest/train/getting-started-pytorch-lightning.html
  - https://docs.ray.io/en/latest/train/getting-started-transformers.html
  - https://docs.ray.io/en/latest/train/user-guides/checkpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lightning and Transformers

Lightning:
```python
import pytorch_lightning as pl
import ray.train
import ray.train.lightning
from ray.train.torch import TorchTrainer

def train_func():
    trainer = pl.Trainer(
        max_epochs=10, devices="auto", accelerator="auto",
        strategy=ray.train.lightning.RayDDPStrategy(),
        plugins=[ray.train.lightning.RayLightningEnvironment()],
        callbacks=[ray.train.lightning.RayTrainReportCallback()],
        enable_checkpointing=False)          # optional: rely on the Ray callback instead
    trainer = ray.train.lightning.prepare_trainer(trainer)
    trainer.fit(MyLitModel(), train_dataloaders=loader)

result = TorchTrainer(train_func, scaling_config=ray.train.ScalingConfig(num_workers=2, use_gpu=True)).fit()
```
Transformers:
```python
import transformers
import ray.train.huggingface.transformers as rt

def train_func():
    trainer = transformers.Trainer(model=model, args=args, train_dataset=ds)  # args with save_strategy="epoch"
    trainer.add_callback(rt.RayTrainReportCallback())
    trainer = rt.prepare_trainer(trainer)
    trainer.train()
```

## Facts from the docs
- Ray Train sets up the distributed process group on each worker before your training function runs, so put all training logic inside the function.
- Lightning: Ray strategies (`RayDDPStrategy`, `RayDeepSpeedStrategy`, and others) subclass Lightning's and accept the same arguments; `RayDDPStrategy` disables `process_group_backend`, `timeout` and `start_method`, which you set in `TorchConfig` instead. `RayLightningEnvironment` configures local/global/node rank and world size. `TorchTrainer` already sets `CUDA_VISIBLE_DEVICES`, so use `devices="auto"` and `accelerator="auto"`. `prepare_trainer` validates the configuration.
- `RayTrainReportCallback` (Lightning) reports on `on_train_epoch_end`; the saved file name is `RayTrainReportCallback.CHECKPOINT_NAME` inside `result.checkpoint`. It can also take `checkpoint_upload_mode` and `validation` flags.
- Transformers: `RayTrainReportCallback` reports whenever the `Trainer` saves a checkpoint, with the latest logged metrics; change frequency with `save_strategy` and `save_steps`. `prepare_trainer` integrates the Trainer with Ray Data.
- DeepSpeed ZeRO: the Ray Train DeepSpeed guide shows each worker saving its shards with `model.save_checkpoint` and reporting them; install `deepspeed` yourself.

## Verify
`result.metrics` holds the reported metrics and `result.checkpoint` contains the Lightning checkpoint file.

## Checked
2026-11-03. Confirmed in Ray repo `train/getting-started-pytorch-lightning.md`, `getting-started-transformers.md`, `deepspeed.md`, `user-guides/checkpoints.md`. Removed: `enable_progress_bar=False` interleaving claim, `deepspeed="ds_config.json"` / working_dir tip, `NCCL_SOCKET_IFNAME` tip, "do not call init_process_group" (rephrased to what the docs state), fixed `accelerator="gpu"`.
Method: documentation only; no commands were run.
