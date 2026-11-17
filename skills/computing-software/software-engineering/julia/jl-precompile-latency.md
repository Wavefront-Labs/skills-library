---
id: computing-software.software-engineering.julia.jl-precompile-latency
name: jl-precompile-latency
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-compile-latency, precompile-latency]
level: advanced
status: docs-checked
description: "Reduce first-call latency with PrecompileTools workloads and PackageCompiler sysimages and apps."
sources: ["https://julialang.github.io/PrecompileTools.jl/stable/", "https://julialang.github.io/PackageCompiler.jl/stable/sysimages.html", "https://julialang.github.io/PackageCompiler.jl/stable/apps.html", "https://docs.julialang.org/en/v1/manual/command-line-interface/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Precompilation and reducing time to first x
- PrecompileTools.jl `@compile_workload` (with `@setup_workload` for setup code) caches compiled code when the package is precompiled; `--pkgimages` on the command line controls native code caching in package images.
- `PackageCompiler.create_sysimage(["Example"]; sysimage_path = "s.so")` builds a custom sysimage; start with `julia -J s.so`; `create_app(src, dest)` bundles an app with its libraries for the same Julia version.
- The SnoopCompile package provides diagnostics for invalidations and missing calls in a workload.
Verify: time the first call of the workload before and after.

## Checked

2026-11-03. Confirmed against: the PrecompileTools page (`@compile_workload`, `@setup_workload`, SnoopCompile diagnostics), PackageCompiler sysimages and apps pages (`create_sysimage`, `-J`, `create_app`) and Manual Command-line Interface (`--pkgimages`). Removed: the `__precompile__()` default claim, the "Julia 1.9 caches native code" claim, and Revise.jl with its struct-redefinition note (not on the pages read); the description no longer mentions Revise or precompile statements.
Method: documentation only; no commands were run.
