---
id: computing-software.software-engineering.julia.jl-run-commands
name: jl-run-commands
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-process, run-commands]
level: practitioner
status: docs-checked
description: "Run external commands with backticks without shell injection, capture output and build pipelines."
sources: ["https://docs.julialang.org/en/v1/manual/running-external-programs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cmd objects, run, read and pipelines
- `` run(`ls -l`) `` runs without a shell; interpolate safely `` `git log $(branch)` `` (an interpolated value stays one argument); `read(cmd, String)` captures stdout; `readchomp(cmd)` strips the newline.
- Pipelines: `` pipeline(`a`, `b`) `` or `` pipeline(`a`; stdout = "out.txt") ``; shell features need `` `sh -c "..."` ``.
- Failure throws `ProcessFailedException`; use `success(cmd)` to test, `ignorestatus(cmd)` to continue.
- Environment and directory: `` setenv(cmd, "K" => "v") `` and `` Cmd(cmd; dir = "x") ``; `ENV["HOME"]` reads variables.
Verify: pass an argument containing spaces and quotes and see it arrive intact.

## Checked

2026-11-02. Confirmed against: Manual Running External Programs page: Cmd objects, interpolation, pipeline, sh -c, setenv, dir, ignorestatus, ProcessFailedException, readchomp. Removed: nothing.
Method: documentation only; no commands were run.
