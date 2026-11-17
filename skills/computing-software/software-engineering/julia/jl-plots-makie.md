---
id: computing-software.software-engineering.julia.jl-plots-makie
name: jl-plots-makie
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-plotting, plots-makie]
level: practitioner
status: draft
description: "Choose between Plots.jl and Makie, create and save figures and manage first-plot latency."
sources: ["https://docs.julialang.org/en/v1/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plots.jl and Makie basics
- Plots.jl: `plot(x, y, label = "a")`, `plot!` to add, `savefig("p.png")`, backends via `gr()`, `plotlyjs()`.
- Makie (CairoMakie for static, GLMakie for interactive): `fig = Figure(); ax = Axis(fig[1, 1]); lines!(ax, x, y); save("p.png", fig)`.
- Time to first plot is long; use a sysimage or keep the session open.
- Headless servers: set `GKSwstype=100` for GR, or use CairoMakie.
Verify: the saved file opens and has the expected size.
