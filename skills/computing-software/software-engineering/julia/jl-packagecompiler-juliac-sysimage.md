---
id: computing-software.software-engineering.julia.jl-packagecompiler-juliac-sysimage
name: jl-packagecompiler-juliac-sysimage
category: computing-software
field: software-engineering
product: julia
tags: [julia, packagecompiler-juliac-sysimage]
level: advanced
status: draft
description: "Cut Julia startup with PackageCompiler sysimages and apps, and know the --trim / juliac option (confirm version)."
sources: ["https://docs.julialang.org/en/v1/manual/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sysimages and apps
- `using PackageCompiler; create_sysimage([:Plots]; sysimage_path="s.so", precompile_execution_file="warm.jl")`; start with `julia -J s.so`.
- `create_app("MyApp", "out")` bundles a relocatable app.
- Julia 1.12 adds `juliac` with `--trim` for smaller executables (confirm status for your version).
- `__precompile__`, `PrecompileTools.@compile_workload` reduce first-call latency without sysimages.
Verify: time `julia -J s.so -e 'using Plots; plot(1:3)'` vs default.
