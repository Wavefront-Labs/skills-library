---
id: computing-software.software-engineering.julia.jl-string-handling
name: jl-string-handling
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-strings, string-handling]
level: practitioner
status: docs-checked
description: "Index strings by byte, iterate by character and format with interpolation, join, split, parse and Printf."
sources: ["https://docs.julialang.org/en/v1/manual/strings/", "https://docs.julialang.org/en/v1/base/strings/", "https://docs.julialang.org/en/v1/base/numbers/", "https://docs.julialang.org/en/v1/stdlib/Printf/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UTF-8 indexing, interpolation and parsing
- Strings are UTF-8 and indexed by byte; `s[i]` raises `StringIndexError` if `i` is not a character start. Use `eachindex(s)`, `nextind`, `collect(s)`, or `first(s, n)`.
- `"x = $x"`, `"$(a + b)"`; `join(xs, ", ")`, `split(s, ',')`, `strip`, `replace(s, "a" => "b")`; `*` concatenates, `repeat` repeats.
- `parse(Int, s)` raises an error on bad input; `tryparse(Int, s)` returns `nothing`.
- Triple-quoted strings are dedented to the least-indented line; `raw"..."` (`@raw_str`) avoids escapes; `Printf.@printf` and `@sprintf` give C-style formats.
Verify: test with multi-byte characters like `"é"` and emoji.

## Checked

2026-11-03. Confirmed against: Manual Strings (byte indexing, StringIndexError, nextind, eachindex, interpolation, `*` concatenation, repeat, triple-quote dedent), Base Strings (first, split, strip, replace, join, nextind, `@raw_str`), Base Numbers (parse, tryparse) and the Printf page (`@printf`, `@sprintf`). Removed: the `^` repeat operator (not in the pages read) and a corrupted raw-string example.
Method: documentation only; no commands were run.
