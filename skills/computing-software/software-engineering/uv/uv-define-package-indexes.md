---
id: computing-software.software-engineering.uv.uv-define-package-indexes
name: uv-define-package-indexes
category: computing-software
field: software-engineering
product: uv
tags: [uv, package-indexes, index, extra-index-url, default-index, explicit-index, pyproject]
level: practitioner
status: docs-checked
description: "Define extra, default, named and explicit package indexes in uv with [[tool.uv.index]], and map them to --index and --index-url flags."
sources: [https://docs.astral.sh/uv/concepts/indexes/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Define package indexes in uv

Goal: add private or alternate indexes to a uv project without surprises about priority.

## Method

Add an entry to `pyproject.toml` (`name` optional, `url` required):

```toml
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"
```

- Priority: indexes are consulted in the order defined; command-line indexes beat config-file ones.
- PyPI is the implicit "default" index, used when a package is on no other index. Remove PyPI by adding `default = true` to another entry (or `--default-index`). The default index is always lowest priority, wherever it sits in the list.
- Names may contain only ASCII alphanumerics, dashes, underscores and periods.
- Command line / environment: `--index`, `--default-index`, `UV_INDEX`, `UV_DEFAULT_INDEX` accept a URL, a configured name, or `<name>=<url>`:

```shell
$ uv lock --index pytorch=https://download.pytorch.org/whl/cpu
$ UV_INDEX=pytorch=https://download.pytorch.org/whl/cpu uv lock
```

- With `--preview-features index-by-name`, configured index names take precedence over matching paths.
- Explicit indexes: `explicit = true` stops packages being installed from that index unless pinned to it (see uv-pin-package-to-index). An index with both `default = true` and `explicit = true` is explicit (usable only via `tool.uv.sources`) and still removes PyPI as default.
- Pip-style flags: `--index-url` equals `--default-index`; `--extra-index-url` equals `--index`. They behave like unnamed `[[tool.uv.index]]` entries (with `default = true` for `--index-url`) and follow the same priority rules, and can be combined with config entries.

## Gotchas

- Named indexes referenced from `tool.uv.sources` must be defined in the project's `pyproject.toml`; indexes from the command line, environment variables or user-level configuration are not recognized there.
- Index credentials: see uv-index-authentication.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/indexes). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
