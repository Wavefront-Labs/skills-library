---
id: computing-software.software-engineering.julia.jl-pkg-environments
name: jl-pkg-environments
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-packages, pkg-environments]
level: practitioner
status: docs-checked
description: "Create reproducible environments with Pkg, commit Manifest correctly and use compat bounds."
sources: ["https://pkgdocs.julialang.org/v1/environments/", "https://pkgdocs.julialang.org/v1/toml-files/", "https://pkgdocs.julialang.org/v1/creating-packages/", "https://docs.julialang.org/en/v1/manual/environment-variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project.toml, Manifest.toml and activate
- `] activate .`, `] add Pkg`, `] instantiate` (install exactly the manifest), `] status`, `] up`, `] resolve`.
- `Project.toml` lists deps and `[compat]`; `Manifest.toml` records exact versions; check it in when you want reproducible installs.
- Add `[compat]` entries for dependencies; registering in the General registry checks for proper version bounds (Creating Packages).
- `Pkg.add(name = "X", version = "1.2")`, `] pin X`, `] develop path`; `JULIA_DEPOT_PATH` sets the depot path.
Verify: `] instantiate` in a clean clone then run tests.

## Checked

2026-11-02. Confirmed against: Pkg docs (Environments, Project.toml and Manifest.toml, Creating Packages) and manual Environment Variables (JULIA_DEPOT_PATH). Removed: the JULIA_PKG_SERVER aside, the stacked-environment advice and the library/application manifest rule.
Method: documentation only; no commands were run.
