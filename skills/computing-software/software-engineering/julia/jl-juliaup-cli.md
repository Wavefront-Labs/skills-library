---
id: computing-software.software-engineering.julia.jl-juliaup-cli
name: jl-juliaup-cli
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-install, juliaup-cli]
level: practitioner
status: docs-checked
description: "Install and switch Julia versions with juliaup, configure startup.jl and use CLI flags, ARGS and @main."
sources: ["https://docs.julialang.org/en/v1/manual/command-line-interface/", "https://github.com/JuliaLang/juliaup"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# juliaup, startup.jl and command-line options
- `juliaup add 1.10`, `juliaup default release`, `julia +1.10 script.jl` switch channels.
- Flags: `--project=.`, `-t auto` (`--threads`), `-O`, `--check-bounds=yes`, `-e "code"`, `--startup-file=no`; `ARGS` holds script arguments.
- `~/.julia/config/startup.jl` runs at start-up (under `$JULIA_DEPOT_PATH/config` if that is set); skip it in CI with `--startup-file=no`.
- Julia 1.11 added `@main` for script entry points.
Verify: `julia --project -e 'using Pkg; Pkg.status()'`.

## Checked

2026-11-03. Confirmed against: Manual Command-line Interface (flags, `ARGS`, `--startup-file`, startup.jl location, `@main` in 1.11) and the juliaup README (`add`, `default`, `+channel`). Removed: the claim that startup.jl loads Revise, the shebang line, and `versioninfo()`/`Base.julia_cmd()` (not on the pages read).
Method: documentation only; no commands were run.
