---
id: computing-software.software-engineering.uv.uv-cache-ci-dynamic-metadata
name: uv-cache-ci-dynamic-metadata
category: computing-software
field: software-engineering
product: uv
tags: [uv, caching, cache-keys, ci-cache, cache-prune, dynamic-metadata, reinstall-package, setuptools-scm]
level: practitioner
status: docs-checked
description: "Control when uv rebuilds local packages with tool.uv.cache-keys and reinstall-package, and trim the cache for CI with uv cache prune --ci."
sources: [https://docs.astral.sh/uv/concepts/cache/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv cache keys for dynamic metadata, and CI caching

Goal: rebuild local packages when dynamic metadata changes, and keep a lean CI cache.

## Method

Default heuristic: uv rebuilds and reinstalls local directory dependencies (such as editables) only if `pyproject.toml`, `setup.py` or `setup.cfg` in the root changed, or a `src` directory was added or removed. This can reinstall less than you want.

Add keys with `tool.uv.cache-keys`. Setting it replaces the defaults, so keep `pyproject.toml` in the list.

```toml
[tool.uv]
# setuptools-scm version: rebuild on commit change
cache-keys = [{ file = "pyproject.toml" }, { git = { commit = true } }]
# also track tags
cache-keys = [{ file = "pyproject.toml" }, { git = { commit = true, tags = true } }]
# dependencies read from requirements.txt
cache-keys = [{ file = "pyproject.toml" }, { file = "requirements.txt" }]
# glob (crate glob syntax)
cache-keys = [{ file = "**/*.toml" }]
# environment variable
cache-keys = [{ file = "pyproject.toml" }, { env = "MY_ENV_VAR" }]
# directory creation or removal
cache-keys = [{ file = "pyproject.toml" }, { dir = "src" }]
```

(These are alternatives; a table can hold `cache-keys` only once.) The `dir` key tracks only the directory itself, not changes inside it. Globs can be expensive because uv may traverse large trees.

Escape hatch for dynamic metadata not covered: always rebuild and reinstall every run:

```toml
[tool.uv]
reinstall-package = ["my-package"]
```

CI caching: by default uv caches both wheels built from source and pre-built wheels it downloads. In CI it is often faster to omit pre-built wheels (re-download them) while keeping source-built wheels, since building extension modules is costly. Run at the end of the job:

```console
$ uv cache prune --ci
```

It removes pre-built wheels and unzipped source distributions, and keeps wheels built from source. The GitHub integration guide has an example.

## Gotchas

- The page recommends running `uv cache prune --ci` at the end of the CI job for maximum cache efficiency.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/cache). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
