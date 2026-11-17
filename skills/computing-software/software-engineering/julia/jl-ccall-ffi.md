---
id: computing-software.software-engineering.julia.jl-ccall-ffi
name: jl-ccall-ffi
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-interop, ccall-ffi]
level: advanced
status: docs-checked
description: "Call C with @ccall, use Cstring and Ptr types, protect memory with GC.@preserve and pass callbacks with @cfunction."
sources: ["https://docs.julialang.org/en/v1/manual/calling-c-and-fortran-code/", "https://docs.julialang.org/en/v1/base/c/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @ccall, C types and callbacks
- `@ccall getenv("SHELL"::Cstring)::Cstring` calls a C function; use `Cstring`, `Csize_t` and `Ptr{...}` types that match the C signature.
- `GC.@preserve` keeps Julia memory alive while C holds a pointer to it.
- Callbacks: `@cfunction(f, Cint, (Cint,))`; the callback must not throw a Julia exception.
Verify: call with a small known input and compare the result to the C documentation.

## Checked

2026-11-03. Confirmed against: Manual Calling C and Fortran Code (`@ccall`, `Cstring`, `Csize_t`, `Ptr`, `GC.@preserve`, `@cfunction`, no exceptions through callbacks) and Base C (`Cstring`, `GC.@preserve`). Removed: the `(:strlen, "libc")` `ccall` form, `unsafe_wrap`, `Libdl.dlopen`, `_jll`/BinaryBuilder.jl, PythonCall.jl/CondaPkg.jl/PyCall.jl/RCall.jl, "types must match exactly" and the `--check-bounds=yes` verify step; the heading and description no longer mention them.
Method: documentation only; no commands were run.
