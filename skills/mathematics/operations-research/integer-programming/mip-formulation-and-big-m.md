---
id: mathematics.operations-research.integer-programming.mip-formulation-and-big-m
name: mip-formulation-and-big-m
category: mathematics
field: operations-research
product: integer-programming
tags: [operations-research, integer-programming, mixed-integer-programming, mip, milp, binary-variables, big-m, indicator-constraints, fixed-charge, facility-location, logical-constraints, either-or-constraints, branch-and-bound, lp-relaxation, mip-gap, cutting-planes, valid-inequalities, symmetry-breaking, formulation-strength, pulp, or-tools, gurobi, cplex, highs]
level: advanced
status: gated
description: "Model yes/no decisions as a MIP: binaries for fixed costs and logic, tight big-M values, stronger formulations, and how to read branch-and-bound gap and bound."
sources:
  - https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html
  - https://developers.google.com/optimization/cp/cp_solver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MIP formulation and big-M

**Goal:** encode discrete decisions (open / don't open, assign / don't, either-or)
in a mixed-integer programme that solves fast enough, because formulation quality
matters more than solver choice.

## 1. Logic to linear: the standard toolkit
y, y₁, y₂ binary; x continuous with known upper bound U.
| Logic | Constraint(s) |
|---|---|
| x can be positive only if y = 1 (fixed charge) | x ≤ U·y, objective + f·y |
| At most one of several options | Σ yᵢ ≤ 1 |
| If y₁ then y₂ | y₁ ≤ y₂ |
| Minimum lot: x = 0 or L ≤ x ≤ U | L·y ≤ x ≤ U·y |
| Either a·x ≤ b or c·x ≤ d | a·x ≤ b + M₁·y,  c·x ≤ d + M₂(1 − y) |
| z = y₁ AND y₂ | z ≤ y₁, z ≤ y₂, z ≥ y₁ + y₂ − 1 |
| Product z = y·x (x ∈ [0, U]) | z ≤ U·y, z ≤ x, z ≥ x − U(1 − y), z ≥ 0 |
| Count k of n events | Σ yᵢ = k |

## 2. Choosing big-M: as small as is valid
M must be large enough never to cut off a feasible solution, and no larger.
- Derive it from data: for x ≤ M·y, M = the true maximum x can take (capacity,
  total demand, min of the two) — **not 1e6**.
- Huge M gives a weak LP relaxation (y = x/M ≈ tiny fraction) and numerical trouble:
  with M = 1e6 and integrality tolerance ~1e-5 (Gurobi `IntFeasTol` default 1e-5; HiGHS 1e-6), y = 1e-6 "counts as 0" yet allows x = 1.
- Prefer solver **indicator constraints** where available (Gurobi `addGenConstrIndicator`,
  CPLEX (gated: unconfirmed, source is paywalled or blocked), OR-Tools CP-SAT `OnlyEnforceIf`, also spelled `only_enforce_if` in current ortools; both run) when no tight M exists.

## 3. Why formulation strength matters
Branch and bound solves LP relaxations; the closer the relaxation is to the integer
hull, the less branching. Example — facility location with facilities i, customers j:
- **Weak (aggregated):** Σⱼ xᵢⱼ ≤ n·yᵢ.
- **Strong (disaggregated):** xᵢⱼ ≤ yᵢ for each i, j.
More constraints, but often orders of magnitude faster, because the relaxation can't
"partly open" a facility to serve many customers (checked on a 2-facility, 3-customer instance with fixed cost 10: LP bound 13.0 weak against 17.0 strong). Same idea: add valid inequalities
that cut fractional points without removing integer solutions.

## 4. Break symmetry
Identical machines or vehicles create many equivalent solutions that the solver
explores separately. Add ordering constraints (e.g. y₁ ≥ y₂ ≥ … for identical
facilities, or load₁ ≥ load₂), or aggregate identical items into one integer variable
("how many trucks of type k").

## 5. Reading the solver log
- **Incumbent** — best integer solution found (primal bound).
- **Best bound** — best possible objective from the relaxation tree (dual bound).
- **Gap** = |incumbent − bound| / |incumbent|. Default stopping gap is small (1e-4 in
  Gurobi (`MIPGap`) and HiGHS (`mip_rel_gap`), both confirmed; CPLEX (gated: unconfirmed, source is paywalled or blocked)); in practice set a business tolerance (e.g. 1%) and a time limit.
- If the bound barely moves while incumbents improve, the formulation is weak (tighten it).
  If the bound is good but no incumbents appear, give a warm start or use heuristics emphasis.

## 6. Workflow
1. Solve the LP relaxation first — its objective is a bound and its fractional pattern
   shows weak spots.
2. Start on a small instance, check the solution by hand.
3. Scale up while watching gap vs time.
4. Report solution, objective, final gap and run time — "optimal within 0.8%".

Tools: PuLP/CBC or HiGHS (free), OR-Tools CP-SAT (excellent for pure-integer
scheduling/assignment), Gurobi/CPLEX (commercial, fastest on hard MIPs).

## Gotchas
- Integer variables with large ranges (0–10,000) branch badly; consider continuous if
  rounding error is negligible.
- Equality constraints with big-M create tiny feasible windows and numeric issues.
- Optimal with gap 0 on a toy instance says nothing about real-size run times.
- Uncertain: default gap tolerances and indicator-constraint APIs differ by solver and
  version; check your solver's parameter docs.

## Verify
- [ ] Every binary has a clear yes/no meaning, written down.
- [ ] Every big-M derived from data and justified as a valid bound.
- [ ] LP relaxation solved and compared to the integer optimum (gap at root).
- [ ] Symmetry broken where identical resources exist.
- [ ] Final gap, time limit and solver settings reported with the answer.
