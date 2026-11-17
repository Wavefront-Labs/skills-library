---
id: computing-software.software-engineering.julia.jl-string-indexing-codeunits
name: jl-string-indexing-codeunits
category: computing-software
field: software-engineering
product: julia
tags: [julia, string-indexing-codeunits]
level: advanced
status: docs-checked
description: "Handle Julia UTF-8 strings: byte indexing, nextind, eachindex, Char vs grapheme clusters."
sources: ["https://docs.julialang.org/en/v1/manual/strings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Julia strings
- `s[i]` indexes bytes; invalid index inside a multibyte char throws `StringIndexError`. Use `eachindex(s)`, `nextind`, `thisind`, `first(s,n)`, `collect(s)`.
- `length(s)` counts chars, `ncodeunits(s)` bytes. Graphemes: `Unicode.graphemes(s)`.
- `SubString` avoids copies.
- Interpolation `"$x and $(a+b)"`, `string(a, b)`, `join(v, ", ")`, `repeat`.
Verify: `length("é")` vs `ncodeunits("é")`.

## Checked

2026-11-02. Confirmed against: Manual Strings page: byte indexing, StringIndexError, nextind, thisind, ncodeunits, SubString, interpolation; Base strings docs. Removed: the String(bytes) claim.
Method: documentation only; no commands were run.
