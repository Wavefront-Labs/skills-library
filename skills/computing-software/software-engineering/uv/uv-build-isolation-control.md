---
id: computing-software.software-engineering.uv.uv-build-isolation-control
name: uv-build-isolation-control
category: computing-software
field: software-engineering
product: uv
tags: [uv, build-isolation, extra-build-dependencies, no-build-isolation-package, dependency-metadata, editable-mode, python]
level: advanced
status: docs-checked
description: "Fix packages that fail under PEP 517 build isolation in uv using extra-build-dependencies with match-runtime, no-build-isolation-package, or dependency-metadata."
sources: [https://docs.astral.sh/uv/concepts/projects/config/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling build isolation

Goal: build packages that need extra or runtime-matched build dependencies. By default uv builds in an isolated environment with only the declared build dependencies (PEP 517). Prefer augmenting build dependencies over disabling isolation.

## Method

Augment build dependencies:

```toml
[tool.uv.extra-build-dependencies]
cchardet = ["cython"]
deepspeed = [{ requirement = "torch", match-runtime = true }]
```

- `match-runtime = true` builds against the version of `torch` installed (or to be installed) in the project environment. It only works for packages with static metadata. For dynamic metadata (for example `axolotl`) pin the version yourself: `dependencies = ["axolotl[deepspeed, flash-attn]", "torch==2.6.0"]` and `axolotl = ["torch==2.6.0"]` in `extra-build-dependencies`.
- `[tool.uv.extra-build-variables]` sets build environment variables, e.g. `flash-attn = { FLASH_ATTENTION_SKIP_CUDA_BUILD = "TRUE" }` to resolve a pre-built wheel; omit it if the CUDA toolkit is available, since it can cause an incompatible install.
- Changes to these settings trigger a rebuild of the affected packages.
- Supply metadata to avoid building during resolution:

```toml
[[tool.uv.dependency-metadata]]
name = "flash-attn"
version = "2.6.3"
requires-dist = ["torch", "einops"]
```

`version` is optional for registry packages (applies to all versions) but required for direct URL dependencies such as Git.

Disable isolation per package: `no-build-isolation-package = ["cchardet"]` under `[tool.uv]` or `--no-build-isolation-package` on the command line. uv installs isolation-capable packages first, then these. Build dependencies must then be in the environment, e.g. listed in `dependencies`.

To keep build-only packages out of the final environment, put them in an extra and sync twice:

```console
$ uv sync --extra build
$ uv sync
```

The second sync removes `cython` and `setuptools`. If resolution itself needs them, install first: `uv venv`, `uv pip install torch setuptools`, then `uv sync`.

## Gotchas

- Disabling isolation complicates installs, adds extraneous packages and hurts reproducibility.

## Verify

After `uv sync --extra build` then `uv sync`, the docs' output lists `- cython` and `- setuptools` removed.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/config). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
