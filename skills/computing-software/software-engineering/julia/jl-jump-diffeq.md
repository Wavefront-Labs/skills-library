---
id: computing-software.software-engineering.julia.jl-jump-diffeq
name: jl-jump-diffeq
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-sciml, jump-diffeq]
level: advanced
status: draft
description: "Model optimisation problems with JuMP and solve ODEs with DifferentialEquations.jl."
sources: ["https://docs.julialang.org/en/v1/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JuMP optimisation and DifferentialEquations.jl
- JuMP: `model = Model(HiGHS.Optimizer); @variable(model, x >= 0); @constraint(model, 2x + y <= 10); @objective(model, Max, x + y); optimize!(model); value(x)`; check `termination_status(model)` and `is_solved_and_feasible`.
- ODEs: `prob = ODEProblem(f!, u0, (0.0, 10.0), p); sol = solve(prob, Tsit5())` with `f!(du, u, p, t)` in-place; stiff problems use `Rodas5` or `QNDF`.
- Set `reltol` and `abstol` explicitly; check `sol.retcode == ReturnCode.Success`.
Verify: compare to an analytic solution for a simple case.
