---
id: computing-software.software-engineering.uv.uv-flat-indexes-find-links
name: uv-flat-indexes-find-links
category: computing-software
field: software-engineering
product: uv
tags: [uv, package-indexes, flat-index, find-links, exclude-newer, local-wheels, index]
level: practitioner
status: docs-checked
description: "Use flat indexes (find-links style directories or HTML pages) in uv with format = flat, and set a per-index exclude-newer cutoff."
sources: [https://docs.astral.sh/uv/concepts/indexes/, https://docs.astral.sh/uv/concepts/cache/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv flat indexes and per-index exclude-newer

Goal: install from a directory or HTML page of wheels, and cap upload dates for one index.

## Method

By default each `[[tool.uv.index]]` is a PEP 503 Simple Repository API registry. A flat index is a local directory or HTML page listing wheels and source distributions (pip's `--find-links`). Declare it with `format = "flat"`:

```toml
[[tool.uv.index]]
name = "example"
url = "/path/to/directory"
format = "flat"
```

Flat indexes support the same features as Simple indexes, such as `explicit = true`, and a package can be pinned to one via `tool.uv.sources`.

Per-index cutoff (see uv-reproducible-resolution for exclude-newer itself):

```toml
[[tool.uv.index]]
name = "internal"
url = "https://internal.example.com/simple"
exclude-newer = "7 days"
```

Index values affect only packages served from that index; `exclude-newer-package` overrides still win. If an index lacks `upload-time` metadata, set `exclude-newer = false` on it to disable the cutoff.

## Gotchas

- Caching: uv assumes flat-index (`--find-links`) contents are immutable and caches each file by name. Rebuilding a wheel into the directory under the same name is not picked up until the cache is refreshed (for example `--refresh`, `--refresh-package <pkg>`, or `uv cache clean <pkg>`).

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/indexes; concepts/cache). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
