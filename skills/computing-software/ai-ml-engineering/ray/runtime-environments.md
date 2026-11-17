---
id: computing-software.ai-ml-engineering.ray.runtime-environments
name: runtime-environments
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, runtime-env, pip-packages, working-dir, py-modules]
level: practitioner
status: docs-checked
description: "Ship dependencies and code with Ray runtime_env: pip, uv, conda, working_dir, env_vars, py_modules, excludes, eager_install and per-job or per-task scope."
sources:
  - https://docs.ray.io/en/latest/ray-core/handling-dependencies.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.runtime_env.RuntimeEnv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime environments

```python
ray.init(runtime_env={
    "working_dir": "./src",                 # local dir or archive, 500 MiB max; workers start in their node's copy
    "excludes": ["*.ckpt", "data/"],
    "pip": ["requests", "pandas"],           # or "uv": [...] (alpha feature)
    "env_vars": {"TOKENIZERS_PARALLELISM": "false"},
    "py_modules": ["./mylib"],
})

@ray.remote(runtime_env={"pip": ["emoji"]})          # per-task environment
def f(): ...
```
CLI jobs: `ray job submit --runtime-env-json='{"working_dir":"./","pip":["emoji"]}' -- python train.py`. `--runtime-env` takes a YAML file instead of inline JSON.

## Gotchas
- A per-job environment from `ray.init(runtime_env=...)` is installed eagerly on every node at `ray.init()`; add `"config": {"eager_install": False}` to install on first task or actor instead. Per-task and per-actor environments install when you invoke them.
- Ray starts a new worker for every task or actor that needs a new environment, so loading a cached environment costs about a normal worker start (a few seconds); avoid per-task environments for tiny tasks. Environments are cached on each node under `/tmp/ray/session_latest/runtime_resources`.
- For large or static dependencies, the docs recommend a container image in the cluster launcher and runtime environments for more dynamic cases.
- `conda` environments must have the same Python version as the cluster, and `ray` must not be listed in the `conda` dependencies.
- `working_dir` must be a local directory (500 MiB max), a local archive (500 MiB uncompressed; `excludes` has no effect on archives), a remote archive URI (`.zip`, `.tar.gz`, `.tgz`, `.tar.xz`, no size limit) or a `local://` path that already exists on every node.
- A local `working_dir` cannot be set per task or per actor, only per job in `ray.init()`.
- `excludes` uses `.gitignore` syntax; Ray excludes `.git`, `.venv`, `venv` and `__pycache__` by default.
- Paths to a local `requirements.txt` or `environment.yml` are relative to your local current directory, not to `working_dir`.
- Ray does not guarantee compatibility between tasks and actors with conflicting environments (for example different versions of one `pip` package).

## Verify
Return `emoji.__version__` (or another package from the env) from a task with and without the env, or check `runtime_env_setup-[job_id].log` for the install.

## Checked
2026-11-03: checked against the Ray docs source `core/handling-dependencies.md`. Fixed: per-job environments install eagerly at `ray.init()`, not lazily; conda cannot change the cluster's Python version; local `working_dir` is per job only. Removed the unsourced remote-URI shorthand, relative-read claim and pinned package versions; the `uv` field is documented (alpha).
Method: documentation only; no commands were run.
