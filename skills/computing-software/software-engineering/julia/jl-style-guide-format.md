---
id: computing-software.software-engineering.julia.jl-style-guide-format
name: jl-style-guide-format
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-style, style-guide-format]
level: practitioner
status: docs-checked
description: "Apply the Julia style guide's naming conventions, generic-code advice and type-piracy rule."
sources: ["https://docs.julialang.org/en/v1/manual/style-guide/", "https://docs.julialang.org/en/v1/manual/methods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Julia style guide
- Modules and types `CamelCase`, functions and variables lowercase with underscores only where needed, constants `UPPER_CASE`, mutating functions end in `!`.
- Avoid type piracy (adding methods to Base functions for Base types you do not own).
- Write generic code: accept `Integer` or `AbstractVector` rather than `Int` or `Vector` where the code works for any; avoid over-annotating.
Verify: review new names and method signatures against the style guide.

## Checked

2026-11-03. Confirmed against: Manual Style Guide (naming, `!` convention, generic argument types, duck typing) and Manual Methods (type piracy). Removed: JuliaFormatter.jl, `.JuliaFormatter.toml`, Blue style and CI-format checks (third-party, not on the pages read); the heading and description no longer mention formatting tools.
Method: documentation only; no commands were run.
