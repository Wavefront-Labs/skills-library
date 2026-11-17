---
id: computing-software.software-engineering.uv.uv-pip-compat-resolution
name: uv-pip-compat-resolution
category: computing-software
field: software-engineering
product: uv
tags: [uv, pip-compatibility, pip-differences, pip-compat, index-strategy, pre-releases, requires-python]
level: advanced
status: docs-checked
description: "Know where uv pip resolves differently from pip: index-strategy, pre-releases, URL dependencies, requires-python bounds, package priority, compile defaults."
sources: [https://docs.astral.sh/uv/pip/compatibility/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv pip vs pip: resolution differences

Goal: predict and fix cases where `uv pip` and `uv pip compile` resolve differently from pip and pip-tools.

## Method

- Config: uv ignores `pip.conf` and `PIP_INDEX_URL`. Use uv's own variables (`UV_INDEX_URL`), a `uv.toml`, or a `[tool.uv.pip]` section in pyproject.toml.
- Multiple indexes: uv takes candidates only from the first index containing the package (extra index before the default), to prevent dependency confusion. Opt out with `--index-strategy` or `UV_INDEX_STRATEGY`: `first-index` (default), `unsafe-first-match`, `unsafe-best-match` (closest to pip, risks dependency confusion). uv also supports pinning a package to a dedicated index so it is always installed from that index.
- Pre-releases: default `if-necessary` prefers stable and falls back to pre-releases only if every stable candidate is rejected. `--prerelease allow` considers all; `disallow` excludes them; `explicit` allows pre-releases only for first-party requirements that name a pre-release.
- Build isolation: PEP 517 isolation is on by default. If a build dependency is missing, try a newer package version, else preinstall build deps and use `uv pip install wheel && uv pip install --no-build-isolation biopython==1.77`.
- Transitive URL dependencies: uv assumes registry packages do not depend on URLs and rejects those that do. A URL in a `--constraint` or `--override` may also cause rejection of a transitive URL. Fix by listing the URL as a direct dependency in pyproject.toml or requirements.in.
- Resolution strategy: both tools give valid but possibly different resolutions. If they differ badly, tighten specifiers (for `starlette` and `fastapi`, require `fastapi>=0.110.0`).
- Package priority: user order matters more to uv, so `uv pip install foo bar` can resolve differently from `bar foo`, and file order affects `uv pip compile`.
- `requires-python`: only lower bounds count (`>=3.8, <4` is treated as `>=3.8`). Versions are truncated to major.minor.patch, so `>=3.13` accepts 3.13.0b1.
- Constraints: `--constraint` / `UV_CONSTRAINT` are not applied to build dependencies; use `--build-constraint` / `UV_BUILD_CONSTRAINT`.
- `uv pip compile` defaults: no output file unless `-o`; extras stripped (`--no-strip-extras` keeps them); no index URLs written unless `--emit-index-url` (then all, including the default).

## Gotchas

- `uv pip check` reports a missing or unparsable METADATA, a Requires-Python lower bound excluding the interpreter, missing or incompatible dependencies, and multiple installed versions of one package (pip check does not flag the last).

## Verify

By default `uv pip compile` writes no output file; pass `-o requirements.txt` (or `--output-file`) to write one.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (pip/compatibility). Removed or changed: removed an unconfirmed "safer route" claim for index pinning (reworded to the page statement) and an unconfirmed stdout claim in Verify (the page says only that no output file is written without -o).

Method: documentation only; no commands were run.
