---
id: computing-software.ai-ml-engineering.model-training.wandb-sweeps
name: wandb-sweeps
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, wandb-sweeps, weights-and-biases, hyperparameter-search, bayesian-optimization, hyperband, wandb-agent]
level: practitioner
status: docs-checked
description: "Run hyperparameter searches with W&B Sweeps: YAML config, grid/random/Bayes methods, Hyperband early termination, agents across GPUs and analysing results."
sources:
  - https://docs.wandb.ai/guides/sweeps/
  - https://docs.wandb.ai/guides/sweeps/define-sweep-configuration/
  - https://docs.wandb.ai/guides/sweeps/parallelize-agents/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# W&B Sweeps

## 1. Training script reads config from wandb
```python
import wandb
def main():
    run = wandb.init()                              # inside a sweep, config is injected
    cfg = run.config
    model = build(cfg.layers, cfg.dropout)
    for epoch in range(cfg.epochs):
        tr_loss = train_epoch(model, lr=cfg.lr, bs=cfg.batch_size)
        val = evaluate(model)
        wandb.log({"epoch": epoch, "train/loss": tr_loss, "val/accuracy": val})
if __name__ == "__main__": main()
```
The metric name in the sweep config must match a logged key exactly.

## 2. Sweep config
```yaml
# sweep.yaml
program: train.py
method: bayes                 # grid | random | bayes
metric: {name: val/accuracy, goal: maximize}
parameters:
  lr: {values: [1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2]}
  batch_size: {values: [32, 64, 128]}
  dropout: {distribution: uniform, min: 0.0, max: 0.5}
  layers: {values: [2, 3, 4]}
  epochs: {value: 20}
early_terminate: {type: hyperband, min_iter: 3, eta: 3}
command: ['${env}', python, '${program}', '${args}']
```
- `method` picks the search strategy (`grid`, `random`, `bayes`); check the sweep-configuration page for the continuous distributions available (it lists quantised variants such as `q_log_uniform_values`).
- Hyperband (`early_terminate`) stops poorly performing runs at brackets derived from `min_iter` and `eta`: with `min_iter: 3, eta: 3` the brackets are 3, 9, 27, 81 iterations; runs must log the metric each epoch.

## 3. Launch agents
```bash
wandb sweep --project myproj sweep.yaml          # prints SWEEP_ID (entity/project/id)
CUDA_VISIBLE_DEVICES=0 wandb agent entity/myproj/abc123 &
CUDA_VISIBLE_DEVICES=1 wandb agent entity/myproj/abc123 &
```
Or in Python: `sweep_id = wandb.sweep(cfg, project="myproj"); wandb.agent(sweep_id, function=main, count=20)`. Agents pointed at the same sweep ID pull from it in parallel; the W&B server chooses parameters. Parallel agents on one machine: set `CUDA_VISIBLE_DEVICES` per agent.
On Slurm/Kubernetes, start one agent per GPU job; W&B Launch can queue sweeps onto compute.

## 4. Analyse
Use the sweep page in the W&B app to compare runs; check the W&B docs for the export API.

## Gotchas
- Set a run budget (`count` in `wandb.agent`) so an agent does not run indefinitely.
- Re-run top configs with different seeds before choosing; sweeps optimise noisy single runs.

## Checked

2026-11-02. Confirmed against the W&B Sweeps overview, Define sweep configuration and Parallelize agents pages: `wandb sweep --project <name> <config>`; `wandb agent <sweep-ID>`; `wandb.agent(sweep_id, function=main, count=4)`; methods grid, random and bayes; `early_terminate` type hyperband with `min_iter` and `eta` (brackets 3, 9, 27, 81 for min_iter 3, eta 3); the `${env}` command macro; `CUDA_VISIBLE_DEVICES` for one agent per GPU. Removed as not stated in the fetched pages: the Gaussian-process remark, `log_uniform_values` (pages show only `q_log_uniform_values`), the `--count` agent flag, pause/resume commands, parameter-importance description, the grid-over-continuous rule, the crashed-run retry claim and the Api export one-liner.

Method: documentation only; no commands were run.
