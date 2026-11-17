---
id: computing-software.software-engineering.uv.uv-constraints-overrides
name: uv-constraints-overrides
category: computing-software
field: software-engineering
product: uv
tags: [uv, overrides, constraints, exclude-dependencies, dependency-metadata, resolution, override-dependencies]
level: practitioner
status: docs-checked
description: "Use uv constraints, overrides, scoped overrides, exclusions and dependency-metadata to steer or unblock resolution."
sources: [https://docs.astral.sh/uv/concepts/resolution/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv constraints, overrides, exclusions, metadata

Goal: unblock or steer a resolution without editing upstream packages.

## Method

- Constraints: `--constraint constraints.txt`. They only narrow versions and add no package by themselves; they apply only if the package is already a direct or transitive dependency.
- Overrides replace every declared requirement for a package, so they can expand versions (escape bad upper bounds). If a dependency declares `pydantic>=1.0,<2.0`, the override `pydantic>=1.0,<3` replaces it. Like constraints, global overrides do not add the package. Use `tool.uv.override-dependencies`, or `--override` with a constraints-style file in the pip interface. Multiple overrides for one package must be separated by markers; a marked dependency is replaced unconditionally.
- Scoped override and exclusion (target one package version's dependencies; omit `version` for all versions):

```toml
[tool.uv]
override-dependencies = [
    "foo>1",
    { package = { name = "bar", version = "0.0.5" }, dependencies = ["foo>2"] },
]
exclude-dependencies = ["foo"]
```

- `exclude-dependencies` removes packages from the graph, including direct requirements. Scoped exclusions can pair with scoped overrides to swap one dependency for another. If both match, the exclusion wins. A version-specific entry beats an all-versions entry; a scoped override beats a global one.
- Scoped overrides support registry version specifiers only (no URL, path, Git or explicit indexes).
- Static metadata avoids building source-only packages during resolution:

```toml
[[tool.uv.dependency-metadata]]
name = "chumpy"
version = "0.70"
requires-dist = ["numpy>=1.8.1", "scipy>=0.13.0", "six>=1.11.0"]
```

uv reads only `name`, `version`, `requires-dist`, `requires-python`, `provides-extra`. `version` is optional for registry packages (applies to all versions) but required for direct URL dependencies such as Git.

## Gotchas

- Overrides are a last resort for when you know the package works.
- Building for metadata is slow and needs the package to build on all platforms.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/resolution). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
