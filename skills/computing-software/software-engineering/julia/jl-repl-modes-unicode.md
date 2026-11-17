---
id: computing-software.software-engineering.julia.jl-repl-modes-unicode
name: jl-repl-modes-unicode
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-repl-unicode, repl-modes-unicode]
level: intro
status: docs-checked
description: "Use the REPL's help, pkg and shell modes, ans, Ctrl-R history search and enter Unicode names with tab completion."
sources: ["https://docs.julialang.org/en/v1/stdlib/REPL/", "https://docs.julialang.org/en/v1/stdlib/InteractiveUtils/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REPL modes, help, shell and Unicode completion
- `?` help mode, `]` pkg mode, `;` shell mode; `ans` holds the last result; `Ctrl-R` starts an interactive history search.
- LaTeX tab completion: `\alpha<Tab>` gives the Greek letter; `\pi<Tab>` gives `π`.
- `varinfo()`, `methodswith(T)`, `@edit f(1)` and `apropos("term")` explore code.
- `~/.julia/config/startup.jl` runs customisations at start-up.
Verify: `\pi<Tab>` produces `π`.

## Checked

2026-11-03. Confirmed against: stdlib REPL (modes, `ans`, history search, LaTeX completion), InteractiveUtils (`varinfo`, `methodswith`, `@edit`, `apropos`). Removed: the Ctrl-D exit claim, `\approx` calling `isapprox`, `names(Mod)`, and OhMyREPL.jl/Revise.jl (not on the pages read); the description no longer says "search mode".
Method: documentation only; no commands were run.
