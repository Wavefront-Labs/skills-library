---
id: mathematics.numerical-and-computational-mathematics.mathematica.solving-equations-symbolically-and-numerically
name: solving-equations-symbolically-and-numerically
category: mathematics
field: numerical-and-computational-mathematics
product: mathematica
tags: [mathematica, wolfram-language, wolfram-engine, solve, nsolve, reduce, findroot, dsolve, ndsolve, assumptions, simplify, fullsimplify, conditionalexpression, root-objects, exact-vs-numeric, working-precision, symbolic-computation, computer-algebra, cas, notebooks]
level: practitioner
status: docs-checked
description: "Get correct answers from Mathematica's equation solvers: Solve vs Reduce vs NSolve vs FindRoot, DSolve vs NDSolve, assumptions, exact vs machine numbers, and checking."
sources: ["https://reference.wolfram.com/language/ref/Solve.html", "https://reference.wolfram.com/language/ref/Reduce.html", "https://reference.wolfram.com/language/ref/NDSolve.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Solving equations in Mathematica (symbolically and numerically)

**Goal:** pick the right solver for the job, tell it the domain and assumptions you
actually mean, and confirm the answer — instead of trusting whatever comes back.

## 1. Syntax that trips people
- Equations use `==`; `=` assigns and `:=` defines. `Solve[x^2 = 4, x]` is an error
  (or worse, assigns).
- Square brackets for functions, parentheses only for grouping, curly braces for lists.
  Built-ins are Capitalised (`Sin`, `Exp`, `Pi`, `E`, `I`).
- Solutions come as **rules**: `sol = Solve[x^2 == 4, x]` gives `{{x -> -2}, {x -> 2}}`.
  Use them with `/.`: `x /. sol` → `{-2, 2}`; `f[x] /. First[sol]`.
- Clear stale definitions (`Clear[x]` or `ClearAll["Global`*"]`) — a leftover `x = 3`
  makes every later solve nonsense. Unexpected numbers in output usually mean this.

## 2. Choose the solver
| Situation | Use |
|---|---|
| polynomial/algebraic, want closed forms, generic solutions | `Solve` |
| need *all* cases, inequalities, parameters, quantifiers | `Reduce` |
| polynomial, want all numeric roots | `NSolve` |
| transcendental, want one root near a guess | `FindRoot[f[x] == 0, {x, x0}]` |
| ODE/PDE closed form | `DSolve` |
| ODE/PDE numeric | `NDSolve` (returns `InterpolatingFunction`) |

`Solve` returns *generic* solutions: it may silently drop special parameter values (e.g.
`a == 0`). `Reduce` returns the full logical case split — use it when parameters are
involved and correctness matters.

## 3. Domains and assumptions
- Default domain is complex. Restrict: `Solve[x^4 == 1, x, Reals]`, or
  `Solve[..., x, Integers]`.
- Simplification needs assumptions to cancel things like `Sqrt[x^2]`:
  `Simplify[Sqrt[x^2], x > 0]` or `Assuming[x > 0 && n ∈ Integers, FullSimplify[expr]]`.
  Without them Mathematica is (correctly) conservative.
- Integrals may return `ConditionalExpression[..., Re[a] > 0]`; supply
  `Assumptions -> a > 0` or read the condition — it is part of the answer.

## 4. Exact vs numeric
- `1/3` is exact; `0.333` is a machine real; `N[expr, 30]` gives 30 digits of arbitrary
  precision. One machine number contaminates the whole expression to machine precision.
- High-degree polynomial roots may come back as exact algebraic-number objects rather than radicals. Use `N` to see values; they are not a failure.
- Ill-conditioned problems: set `WorkingPrecision -> 30` (and give exact inputs) in
  `FindRoot`, `NIntegrate`, `NDSolve` to check digits. 
- `FindRoot` finds one root from your start; plot first (`Plot[f[x], {x, a, b}]`) to choose
  starting points and to see how many roots exist.

## 5. NDSolve essentials
`sol = NDSolve[{y''[t] + y[t] == 0, y[0] == 1, y'[0] == 0}, y, {t, 0, 10}];
Plot[Evaluate[y[t] /. sol], {t, 0, 10}]`
- `Evaluate` inside `Plot` avoids re-solving at every point.
- NDSolve warning messages usually indicate a singularity or stiffness; read them.
- Control accuracy with `AccuracyGoal` (absolute local error), `PrecisionGoal` (relative local error) and `MaxSteps`.

## 6. Check every answer
- Substitute back: `eqn /. sol // Simplify` should give `True`s (exact) or tiny residuals.
- `Reduce` the same problem when `Solve` emits a message about inverse functions or dropped solutions.
- Numerically spot-check a symbolic result at random parameter values.

## Gotchas
- Messages printed in orange/red are not cosmetic; read each one.
- `Simplify` vs `FullSimplify`: the latter tries more transformations and can be slow.
- Solver behaviour changes between versions; confirm with the docs for your installed version.

## Checked
2026-11-01. Confirmed on the Solve page (generic solutions only; conditionally valid ones as ConditionalExpression), the Reduce page, and the NDSolve page (InterpolatingFunction results; AccuracyGoal absolute, PrecisionGoal relative; MaxSteps). Removed: the Minimize/NMinimize/FindMinimum row, the `$MachinePrecision` figure, specific message names, the StiffnessSwitching method and the Root object name (not found on fetched pages).

Method: documentation only; no commands were run.

## Verify
- [ ] No stale global definitions (fresh kernel or `ClearAll`).
- [ ] Domain and assumptions stated explicitly.
- [ ] Solutions substituted back and confirmed (`True` or residual ≈ 0).
- [ ] Parametric problems checked with `Reduce` for missed special cases.
- [ ] Numeric answers re-run at higher `WorkingPrecision` agree.
