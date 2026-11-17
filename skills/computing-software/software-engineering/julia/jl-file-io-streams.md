---
id: computing-software.software-engineering.julia.jl-file-io-streams
name: jl-file-io-streams
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-io, file-io-streams]
level: practitioner
status: docs-checked
description: "Read and write files safely with open do-blocks, readlines, eachline and path functions."
sources: ["https://docs.julialang.org/en/v1/manual/networking-and-streams/", "https://docs.julialang.org/en/v1/manual/strings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# open, read, write and do-block file handling
- `open("f.txt", "r") do io ... end` closes the file even on error; `read(path, String)`, `readlines(path)`, `eachline(path)` streams.
- `write(io, x)`, `println(io, x)`, `print`, `flush(io)`; `mktemp()`/`mktempdir()` for scratch space.
- Paths: `joinpath`, `dirname`, `basename`, `splitext`, `isfile`, `isdir`, `mkpath`, `rm(p; recursive = true, force = true)`, `@__DIR__`.
- Encoding: strings are UTF-8; read bytes with `read(io)` for binary; `IOBuffer` for in-memory streams.
Verify: round-trip write then read in a temp directory.

## Checked

2026-11-02. Confirmed against: Manual Networking and Streams and Strings pages; Base file and I/O docs for the function names. Removed: nothing.
Method: documentation only; no commands were run.
