---
id: computing-software.ai-ml-engineering.mlflow.running-mlflow-projects-from-git
name: running-mlflow-projects-from-git
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-projects, mlflow-run, git-projects, version-pinning, remote-execution]
level: practitioner
status: docs-checked
description: "Run MLflow Projects straight from Git repositories: URI and subdirectory syntax, pinning commits with --version, private repos, parameters, and remote backends."
sources:
  - https://mlflow.org/docs/latest/ml/projects/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/cli/__init__.py
  - https://github.com/mlflow/mlflow/blob/master/mlflow/projects/__init__.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running MLflow Projects from Git

**Goal:** launch a training run of a specific commit of a repo without manually cloning it, so results trace back to exact code.

## Syntax
```bash
mlflow run https://github.com/org/ml-repo.git#projects/churn --version 3f2c1ab -P alpha=0.4 --experiment-name churn
mlflow run git@github.com:org/ml-repo.git#projects/churn --version v1.7.0
```
- `#subdir` selects a project inside a monorepo (the directory containing `MLproject`).
- `--version` takes a Git commit reference (the docs show a commit hash and a branch name). Pin a commit SHA for reproducibility; a branch name runs whatever is at its tip today.
- MLflow clones into a temp directory, checks out the version, builds the environment, runs the entry point, and records `mlflow.source.git.commit` and `mlflow.source.git.repoURL` on the run.

## Private repositories
Use SSH URLs with an agent/deploy key available to the process, or HTTPS with a credential helper / token in the environment of the machine running `mlflow run`. Don't put tokens in the URI.

## Python API
```python
import mlflow
sub = mlflow.projects.run(
    uri="https://github.com/org/ml-repo.git#projects/churn",
    version="v1.7.0", entry_point="main", parameters={"alpha": 0.4},
    experiment_name="churn", env_manager="virtualenv", synchronous=False,
)
sub.wait(); print(sub.run_id, sub.get_status())
```
`synchronous=False` returns a `SubmittedRun` to launch several runs (a small sweep) in parallel.

## Remote backends
- `backend="databricks", backend_config="cluster.json"` runs on a new job cluster.
- `backend="kubernetes"` requires a `docker_env` project, a `kubernetes_config.json` with the context and job template, and pushes an image built from the project.

## Gotchas
- Uncommitted local changes are not included when running a Git URI - commit and push first (or run `.` locally, where MLflow records a dirty-tree flag).
- Git URIs are cloned for each run; for large repos run from a pre-cloned checkout at a pinned commit.

## Verify
- [ ] Run tags show repo URL and the pinned commit.
- [ ] The same command re-run later produces the same code/environment.
- [ ] No credentials visible in run tags or params.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Git URI forms, `#subdirectory`, `--version <commit hash | branch>`: docs/classic-ml/projects/index.mdx (Git Integration section); `--version` help text, `-P`, `--experiment-name`: mlflow/cli/__init__.py.
- `mlflow.projects.run` parameters and `SubmittedRun` (`wait()`, `get_status()`, `run_id`): mlflow/projects/__init__.py and submitted_run.py. Git tag names `mlflow.source.git.commit`, `repoURL`, `dirty`: mlflow/utils/mlflow_tags.py.
- Databricks backend with a cluster-spec JSON and Kubernetes backend needing `docker_env`: projects docs and `validate_docker_env`.
- Removed as unconfirmed: the statement that tokens in a URI end up in run tags and the shallow-clone advice.

Method: documentation only; no commands were run.
