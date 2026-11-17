---
id: computing-software.software-engineering.julia.jl-pkg-project-manifest-compat
name: jl-pkg-project-manifest-compat
category: computing-software
field: software-engineering
product: julia
tags: [julia, pkg-project-manifest-compat]
level: practitioner
status: docs-checked
description: "Manage environments in Julia: activate, add, instantiate, [compat] bounds, and committing manifests."
sources: ["https://pkgdocs.julialang.org/v1/environments/", "https://pkgdocs.julialang.org/v1/toml-files/", "https://pkgdocs.julialang.org/v1/compatibility/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pkg environments
- `] activate .`, `] add Pkg`, `] instantiate`, `] resolve`, `] up`, `] status`, `] pin`, `] dev path`.
- `Project.toml` holds deps and `[compat]` entries (`Foo = "1.2"` is caret-style).
- From Julia v1.10.8 a file named `Manifest-v{major}.{minor}.toml` is preferred by that Julia version over `Manifest.toml`.
- Run scripts with `julia --project=. script.jl`.
Verify: fresh clone plus `instantiate` reproduces versions.

## Checked

2026-11-02. Confirmed against: Pkg docs: Environments, Project.toml and Manifest.toml (version-specific manifests), Compatibility (caret-style specifiers). Removed: the commit-the-manifest rule for libraries and applications.
Method: documentation only; no commands were run.
