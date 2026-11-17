---
id: computing-software.software-engineering.julia.jl-ccall-pythoncall
name: jl-ccall-pythoncall
category: computing-software
field: software-engineering
product: julia
tags: [julia, ccall-pythoncall]
level: advanced
status: draft
description: "Call C with ccall, Python with PythonCall/PyCall, and R with RCall from Julia."
sources: ["https://docs.julialang.org/en/v1/manual/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interop
- `ccall((:strlen, "libc"), Csize_t, (Cstring,), "hi")`; use `@ccall` macro for readability; `Ref`, `Ptr`, `unsafe_wrap` for arrays.
- PythonCall.jl: `using PythonCall; np = pyimport("numpy"); pyconvert(Vector{Float64}, np.arange(3))`, manages Python via CondaPkg.
- RCall.jl: `R"mean(c(1,2,3))"`.
- Keep `GC.@preserve` around pointers passed to C.
Verify: ccall result matches the C library value.
