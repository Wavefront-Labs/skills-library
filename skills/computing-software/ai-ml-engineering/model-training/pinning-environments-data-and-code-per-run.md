---
id: computing-software.ai-ml-engineering.model-training.pinning-environments-data-and-code-per-run
name: pinning-environments-data-and-code-per-run
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, environment-pinning, data-versioning, lockfiles, experiment-tracking, reproducibility]
level: practitioner
status: draft
description: "Make every training run traceable: lockfiles and container digests, git commit and dirty-state checks, immutable data snapshots with hashes, and logging all of it per run."
sources:
  - https://docs.astral.sh/uv/concepts/projects/sync/
  - https://dvc.org/doc/start/data-management/data-versioning
  - https://mlflow.org/docs/latest/ml/tracking/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pinning environments, data snapshots and code per run

A result you can't rerun is an anecdote. Record four things per run: code, environment, data, config.

## Code
```python
import subprocess
sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
dirty = subprocess.call(["git", "diff", "--quiet"]) != 0
if dirty and not ALLOW_DIRTY: raise SystemExit("commit your changes before a tracked run")
```
Log `sha` and, if dirty is allowed, the diff (`git diff > diff.patch` as an artefact). MLflow and W&B capture the commit automatically when run inside a repo.

## Environment
- Lock exact versions with hashes: `uv lock` / `uv sync --frozen`, `pip-compile --generate-hashes`, `poetry.lock`, `conda-lock`. A `requirements.txt` with `torch>=2` is not a pin.
- Container image by **digest** (`image@sha256:...`), not a mutable tag like `latest`.
- Record what the lockfile can't: CUDA driver, CUDA/cuDNN runtime, GPU model, `torch.__version__`, `torch.version.cuda`, CPU arch. `python -m torch.utils.collect_env` prints most of it.
- Save `pip freeze` output as a run artefact as a fallback record.

## Data
- Train from an **immutable snapshot**, never "the current table". Options: DVC-tracked files (`dvc add`, commit `.dvc` file, `dvc push`), lakeFS commits, Delta/Iceberg time travel (`VERSION AS OF` / snapshot id), dated object-store prefixes with write-once policies.
- Log the snapshot id plus a content hash (e.g. sha256 of the manifest or of sorted file hashes) and row counts per split.
- Log split definitions (seed and method, or the list of IDs per split) so evaluation sets don't drift between runs.
- Feature store training sets: log the feature view versions and the entity dataframe's timestamp range.

## Config
Single resolved config file (Hydra/OmegaConf, YAML) saved as an artefact, including defaults. Command-line overrides logged too.

## Put it together
```python
mlflow.log_params(flat_config)
mlflow.set_tags({"git_sha": sha, "git_dirty": dirty, "image_digest": os.environ.get("IMAGE_DIGEST"),
                 "data_snapshot": snapshot_id, "data_sha256": data_hash, "torch": torch.__version__,
                 "cuda": torch.version.cuda, "gpu": torch.cuda.get_device_name(0)})
mlflow.log_artifact("uv.lock"); mlflow.log_artifact("config.resolved.yaml")
```
Register models with a link back to the run ID so a deployed model traces to all of the above.

## Verify
Pick a past run and rebuild it from its record alone (checkout sha, pull image digest, fetch data snapshot, run config): metrics should match within run-to-run variance.
