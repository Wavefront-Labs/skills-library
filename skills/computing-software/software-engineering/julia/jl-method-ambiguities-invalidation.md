---
id: computing-software.software-engineering.julia.jl-method-ambiguities-invalidation
name: jl-method-ambiguities-invalidation
category: computing-software
field: software-engineering
product: julia
tags: [julia, method-ambiguities-invalidation]
level: advanced
status: docs-checked
description: "Find and fix ambiguous methods with Test.detect_ambiguities and avoid type piracy; invalidations are diagnosed with SnoopCompile."
sources: ["https://docs.julialang.org/en/v1/manual/methods/", "https://docs.julialang.org/en/v1/stdlib/Test/", "https://julialang.github.io/PrecompileTools.jl/stable/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ambiguities and invalidations
- An ambiguity arises when two methods match and neither is more specific; define the intersecting signature explicitly. `Test.detect_ambiguities(MyPkg)` finds them (`recursive=true` to include submodules).
- Type piracy (extending a `Base` function on `Base` types) causes surprises.
- Invalidation is diagnosed with `SnoopCompileCore.@snoop_invalidations` from the SnoopCompile package (named on the PrecompileTools page).
Verify: the ambiguity test returns an empty list.

## Checked

2026-11-03. Confirmed against: Manual Methods (ambiguity definition and resolution, type piracy), stdlib Test (`detect_ambiguities`, `recursive`) and the PrecompileTools page (`SnoopCompileCore.@snoop_invalidations` named as the invalidation diagnostic). Removed: the claim that type piracy causes invalidations and the fix advice for invalidations ("narrower signatures or type-stable code"), neither of which is on the pages read.
Method: documentation only; no commands were run.
