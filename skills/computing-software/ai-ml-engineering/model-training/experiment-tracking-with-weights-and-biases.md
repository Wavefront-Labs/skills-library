---
id: computing-software.ai-ml-engineering.model-training.experiment-tracking-with-weights-and-biases
name: experiment-tracking-with-weights-and-biases
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, weights-and-biases, wandb, experiment-tracking, artifacts, model-registry, reproducibility]
level: practitioner
status: draft
description: "Track ML experiments in Weights and Biases: wandb.init config, metrics and media logging, framework integrations, artifacts for data and model lineage, offline mode and reports."
sources:
  - https://docs.wandb.ai/guides/track/
  - https://docs.wandb.ai/guides/artifacts/
  - https://docs.wandb.ai/guides/integrations/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Experiment tracking with Weights and Biases

## Basic run
```python
import wandb
run = wandb.init(project="churn", entity="team", name="lgbm-v3", group="lgbm", job_type="train",
                 tags=["baseline"], config={"lr": 0.05, "num_leaves": 63, "data_version": "2026-10-01"})
for step, (tr, va) in enumerate(train()):
    wandb.log({"train/loss": tr, "val/auc": va}, step=step)
run.summary["best_val_auc"] = best          # headline numbers for the runs table
run.finish()
```
- Put every knob in `config` (including data version and git commit; W&B captures git SHA and diff automatically when run in a repo).
- Use `/` in metric names for panel grouping; define custom x-axes with `wandb.define_metric("val/*", step_metric="epoch")`.
- `summary` overrides the default last-value summary (e.g. best, not last).

## Integrations
- Hugging Face: `TrainingArguments(report_to="wandb", run_name=...)`; `WANDB_PROJECT` env var.
- Lightning: `WandbLogger(project=..., log_model="all")`.
- Keras: `WandbMetricsLogger()`, `WandbModelCheckpoint`.
- XGBoost/LightGBM: `wandb.integration.xgboost.WandbCallback`, `wandb.integration.lightgbm.wandb_callback()`.
- PyTorch: `wandb.watch(model, log="gradients", log_freq=100)` for gradient histograms.

## Media and tables
`wandb.log({"examples": wandb.Table(dataframe=errors_df)})`, `wandb.Image`, `wandb.plot.confusion_matrix(...)`, `wandb.plot.pr_curve(...)`. Tables of worst predictions make error analysis shareable.

## Artifacts (lineage)
```python
art = wandb.Artifact("churn-train", type="dataset", metadata={"rows": len(df)})
art.add_file("train.parquet"); run.log_artifact(art)                    # versioned v0, v1...
data_dir = run.use_artifact("team/churn/churn-train:latest").download()  # records input lineage
model_art = wandb.Artifact("churn-model", type="model"); model_art.add_file("model.txt")
run.log_artifact(model_art, aliases=["best", "staging"])
run.link_artifact(model_art, "team/model-registry/churn")                # registry collection
```
Large data in your bucket: `art.add_reference("s3://bucket/path")` tracks checksums without uploading.

## Operations
- Offline: `WANDB_MODE=offline` then `wandb sync wandb/offline-run-*` later (air-gapped clusters).
- API key via `WANDB_API_KEY` secret, never in code. Self-hosted server available for data residency.
- Distributed training: log from rank 0 only, or use `group` to collect per-rank runs.
- Query programmatically: `wandb.Api().runs("team/churn", filters={"config.lr": 0.05})`.

## Verify reproducibility
From any run page you should find: code version, config, data artifact version, environment (`requirements.txt` captured), and resulting model artifact. If any are missing, add them to `init`/artifacts.
