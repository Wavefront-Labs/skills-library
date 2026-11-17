---
id: computing-software.software-engineering.uv.uv-pin-package-to-index
name: uv-pin-package-to-index
category: computing-software
field: software-engineering
product: uv
tags: [uv, package-indexes, index-strategy, tool-uv-sources, dependency-confusion, explicit-index, index]
level: practitioner
status: docs-checked
description: "Pin a package to a specific uv index with tool.uv.sources, switch indexes by marker, and choose an --index-strategy with its dependency-confusion tradeoffs."
sources: [https://docs.astral.sh/uv/concepts/indexes/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pin packages to an index and pick a search strategy

Goal: guarantee which index serves a package.

## Method

Pin in `tool.uv.sources`:

```toml
[tool.uv.sources]
torch = { index = "pytorch" }

[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
```

`explicit = true` means only pinned packages come from that index; everything else comes from PyPI.

Platform-dependent index, using a list of sources with markers:

```toml
[tool.uv.sources]
torch = [
  { index = "pytorch-cpu", marker = "sys_platform == 'darwin'"},
  { index = "pytorch-cu130", marker = "sys_platform != 'darwin'"},
]
```

(with matching `[[tool.uv.index]]` entries named `pytorch-cpu` and `pytorch-cu130`).

Search strategy across indexes (`--index-strategy` or `UV_INDEX_STRATEGY`):

- `first-index` (default): candidate versions are limited to those on the first index containing the package. If a package exists on an internal index it is never installed from PyPI, which prevents dependency confusion attacks (the `torchtriton` attack of December 2022 is the cited example).
- `unsafe-first-match`: search all indexes but prefer the first one with a compatible version, even if newer versions exist elsewhere.
- `unsafe-best-match`: pick the best version from the combined candidates. Closest to pip, but exposes you to dependency confusion.

## Gotchas

- The index named in `tool.uv.sources` must be defined in the project's `pyproject.toml`; command-line, environment and user-level indexes are not recognized.
- An index marked both `default = true` and `explicit = true` is treated as explicit while still removing PyPI as the default.
- `--index-url` / `--extra-index-url` map to `--default-index` / `--index` and follow the same prioritization.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/indexes). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
