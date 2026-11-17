---
id: computing-software.software-engineering.julia.jl-pkg-develop-register
name: jl-pkg-develop-register
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-packages, pkg-develop-register]
level: advanced
status: docs-checked
description: "Generate a package, write tests, declare extensions and follow semantic versioning before registering."
sources: ["https://pkgdocs.julialang.org/v1/creating-packages/", "https://pkgdocs.julialang.org/v1/repl/", "https://pkgdocs.julialang.org/v1/toml-files/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating, testing and registering packages
- `pkg> generate Foo` creates `Project.toml` (with a `uuid`) and `src/Foo.jl`; the docs recommend PkgTemplates.jl for a fuller layout.
- Tests live in `test/runtests.jl`; `pkg> test` runs them in a temporary environment, with test-only dependencies in `test/Project.toml` or the older `[extras]`/`[targets]`.
- Follow semantic versioning (before 1.0.0, breaking changes increment the minor version).
- Package extensions (`[weakdeps]` and `[extensions]`, Julia 1.9 or newer) add optional integrations without hard dependencies.
Verify: `pkg> test` passes.

## Checked

2026-11-03. Confirmed against: Pkg docs Creating Packages (`generate`, PkgTemplates, tests, extensions, semver), the Pkg REPL page (`test`) and Project.toml reference (`uuid`, `[weakdeps]`, `[extensions]`). Removed: Registrator.jl, TagBot, CI on LTS and latest, and the `Template(...)("Foo")` call (not on the pages read); `test/runtests.jl` is no longer attributed to `generate`; the description no longer says "set up CI and register through the General registry".
Method: documentation only; no commands were run.
