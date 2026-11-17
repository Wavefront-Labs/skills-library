---
id: computing-software.software-engineering.julia.jl-modules-using-import
name: jl-modules-using-import
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-modules, modules-using-import]
level: practitioner
status: docs-checked
description: "Organise code into modules and understand using versus import and name conflicts."
sources: ["https://docs.julialang.org/en/v1/manual/modules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# module, using, import and export
- `module M; export f; f() = 1; end`; `using .M` for a local module, `import .M: f` to extend `f`.
- `using Pkg` brings exported names; resolve name conflicts by qualifying the name (`A.f`) as in the Modules page.
- The `public` keyword (public API that is not exported) needs Julia 1.11.
- `include("file.jl")` evaluates a file in the current module.
Verify: restart Julia to check that load order works in a fresh session.

## Checked

2026-11-02. Confirmed against: Manual Modules page (export, using, import, include, public keyword and its Julia 1.11 requirement, name conflicts). Removed: the include-in-loops advice and the vague conflict wording.
Method: documentation only; no commands were run.
