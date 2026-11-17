---
id: computing-software.software-engineering.julia.jl-docstrings-documenter
name: jl-docstrings-documenter
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-docs, docstrings-documenter]
level: practitioner
status: docs-checked
description: "Write docstrings in the standard format, run jldoctest blocks and build documentation with Documenter's makedocs."
sources: ["https://docs.julialang.org/en/v1/manual/documentation/", "https://documenter.juliadocs.org/stable/man/guide/", "https://documenter.juliadocs.org/stable/man/doctests/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docstrings, doctests and Documenter.jl
- A string literal before a definition is its docstring; start with the signature indented four spaces, then a one-line imperative summary, then details with `# Examples`.
- Fenced `jldoctest` blocks run as tests with `doctest(MyPackage)`; doctest failures are fatal in `makedocs` by default.
- `Documenter.jl` builds documentation with `makedocs(...)`.
- `?name` in the REPL reads docs; `apropos("text")` searches them.
Verify: `doctest(MyPackage)` passes.

## Checked

2026-11-03. Confirmed against: Manual Documentation (docstring layout, `# Examples`), the Documenter guide (`makedocs`) and the Documenter doctests page (`jldoctest`, `doctest`, failing doctests fail `makedocs`), plus the REPL page (`?name`) and InteractiveUtils (`apropos`). Removed: `deploydocs`, `docs/make.jl`, the doctest-filter clause and the "in CI" wording (not confirmed on the pages read).
Method: documentation only; no commands were run.
