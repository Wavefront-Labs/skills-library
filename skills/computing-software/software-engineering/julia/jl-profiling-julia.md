---
id: computing-software.software-engineering.julia.jl-profiling-julia
name: jl-profiling-julia
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-performance, profiling-julia]
level: advanced
status: docs-checked
description: "Profile with the Profile stdlib, read allocation profiles and inspect compiled code with @code_* macros."
sources: ["https://docs.julialang.org/en/v1/manual/profile/", "https://docs.julialang.org/en/v1/stdlib/Profile/", "https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profile and allocation profiling
- `using Profile; @profile f(); Profile.print()` after one warm-up call, so compilation is not profiled.
- `Profile.Allocs.@profile` (Julia 1.8 or newer) samples allocations.
- `@code_llvm`, `@code_native`, `@code_typed` inspect compiled output.
- `--track-allocation=user` writes `.mem` files.
Verify: re-profile after changes to confirm the hot spot moved.

## Checked

2026-11-03. Confirmed against: Manual Profiling (warm-up call, `@profile`, `Profile.print`, `--track-allocation` and `.mem` files), stdlib Profile (`Profile.Allocs.@profile`, 1.8) and InteractiveUtils (`@code_*`). Removed: ProfileView.jl, PProf.jl, VSCode `@profview` and Chairmarks (not on the pages read) from the body and heading.
Method: documentation only; no commands were run.
