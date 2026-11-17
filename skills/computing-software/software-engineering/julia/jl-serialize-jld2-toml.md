---
id: computing-software.software-engineering.julia.jl-serialize-jld2-toml
name: jl-serialize-jld2-toml
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-serialization, serialize-jld2-toml]
level: practitioner
status: docs-checked
description: "Know what the Serialization stdlib guarantees, avoid it for long-term storage of anonymous functions, and read and write TOML."
sources: ["https://docs.julialang.org/en/v1/stdlib/Serialization/", "https://docs.julialang.org/en/v1/stdlib/TOML/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serialization and TOML
- The `Serialization` format can change in minor 1.x releases, but files written by earlier 1.x versions stay readable; the exception is data whose types come from external packages that changed.
- Do not rely on serialized anonymous functions for long-term storage, and note that `deserialize` does not validate its input, so only read trusted data.
- Config: `TOML.parsefile("a.toml")` in the stdlib; `TOML.print(io, dict)` writes.
Verify: reload and `==` compare.

## Checked

2026-11-03. Confirmed against: stdlib Serialization (format change policy, readability of older files, external-package exception, anonymous functions, no validation) and stdlib TOML (`parsefile`, `print`). Real error fixed: the draft said the format is not guaranteed stable across Julia versions, but the page says files from earlier 1.x versions remain readable. Removed: JLD2/FileIO, Arrow.jl, Parquet2.jl and CSV.jl claims (third-party, not on the pages read); the description no longer mentions them.
Method: documentation only; no commands were run.
