---
id: computing-software.software-engineering.julia.jl-regex-julia
name: jl-regex-julia
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-strings, regex-julia]
level: practitioner
status: docs-checked
description: "Use r\"\" literals, match, eachmatch and substitution strings with PCRE semantics."
sources: ["https://docs.julialang.org/en/v1/manual/strings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regular expressions
- `occursin(r"^\d+$", s)`, `m = match(r"(\d+)-(\d+)", s)` returns `nothing` or a `RegexMatch` with `m.captures` and `m[1]`.
- `eachmatch(r, s)` iterates matches; `replace(s, r"(a)(b)" => s"\2\1")` uses the `s""` substitution string.
- Named captures: `(?<year>\d{4})` accessed as `m[:year]`.
- Regex flags go after the literal: `r"abc"i`.
Verify: handle the `nothing` result before indexing.

## Checked

2026-11-02. Confirmed against: Manual Strings page, Regular Expressions section: match, RegexMatch, eachmatch, named captures, s"" substitution, flags. Removed: nothing.
Method: documentation only; no commands were run.
