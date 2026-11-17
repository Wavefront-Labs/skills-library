---
id: computing-software.software-engineering.julia.jl-julia-github-actions
name: jl-julia-github-actions
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-ci, julia-github-actions]
level: practitioner
status: draft
description: "Test a Julia package on multiple versions and platforms with julia-actions and cache dependencies."
sources: ["https://docs.julialang.org/en/v1/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GitHub Actions for Julia packages
- Use `julia-actions/setup-julia`, `julia-actions/cache`, `julia-actions/julia-buildpkg`, `julia-actions/julia-runtest`; matrix versions `lts`, `1`, `pre`.
- `julia-actions/julia-processcoverage` then upload to Codecov; CompatHelper opens PRs for new dependency versions; TagBot makes releases.
- Add Documenter deployment with `DOCUMENTER_KEY`.
Verify: the matrix passes on Linux, macOS and Windows.
