---
id: mathematics.operations-research.linear-programming.lp-formulation-duality-and-sensitivity
name: lp-formulation-duality-and-sensitivity
category: mathematics
field: operations-research
product: linear-programming
tags: [operations-research, linear-programming, lp, optimisation, optimization, formulation, decision-variables, objective-function, constraints, simplex, interior-point, duality, dual-values, shadow-price, reduced-cost, sensitivity-analysis, ranging, infeasible, unbounded, product-mix, blending, transportation-problem, pulp, scipy-linprog, highs, excel-solver]
level: practitioner
status: gated
description: "Formulate a real decision as a linear programme, solve it, and use dual values, reduced costs and ranging to explain the answer and what would change it."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
  - https://pypi.org/project/PuLP/
  - https://docs.gurobi.com/projects/optimizer/en/current/reference/attributes.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# LP formulation, duality and sensitivity

**Goal:** model a resource-allocation decision as an LP correctly, and extract the
management insight — which constraints bind and what relaxing them is worth.

## 1. Formulate in words, then symbols
Write three lists before any code:
1. **Decisions** — quantities you control, with units ("tonnes of product j per week").
2. **Objective** — one linear expression to maximise or minimise.
3. **Constraints** — every limit, each in consistent units.
Example (product mix): x₁, x₂ = units of chairs and tables.
max 30x₁ + 50x₂ subject to wood 2x₁ + 4x₂ ≤ 100, labour 3x₁ + 2x₂ ≤ 90, x ≥ 0.
Optimal: x₁ = 20, x₂ = 15, profit 1,350 (both constraints bind).

Linearity check: no products of variables, no `if`, no `max()` in constraints, no
fixed charges. Those need integer variables (see
mathematics.operations-research.integer-programming.mip-formulation-and-big-m).

## 2. Classic patterns
- **Blending:** fractions of inputs meet quality specs → write specs as
  Σ qᵢxᵢ ≥ q_min·Σ xᵢ (linear), not as a ratio.
- **Transportation:** supply ≤ capacity at each source, demand met at each sink, minimise Σ cᵢⱼxᵢⱼ.
- **Multi-period:** inventory balance I_t = I_{t−1} + produce_t − demand_t.
- **Minimise a maximum or absolute value:** introduce t with t ≥ each term (or
  t ≥ e, t ≥ −e) and minimise t. Works only in the "good" direction (min of max, not max of max).

## 3. Solve
- Python PuLP 3.x (bundles CBC; tested with 3.3.2, so use `pip install "pulp<4"`: PuLP 4.0 is a rewrite where variables come from `m.add_variable` and `pulp.LpStatus` is gone). Expected output for this model: Optimal 20.0 15.0 with duals wood 11.25, labour 2.5:
```python
import pulp
m = pulp.LpProblem("mix", pulp.LpMaximize)
x1 = pulp.LpVariable("chairs", lowBound=0); x2 = pulp.LpVariable("tables", lowBound=0)
m += 30*x1 + 50*x2
m += 2*x1 + 4*x2 <= 100, "wood"
m += 3*x1 + 2*x2 <= 90, "labour"
m.solve(pulp.PULP_CBC_CMD(msg=False))   # bundled CBC; HiGHS_CMD needs a separate highs binary
print(pulp.LpStatus[m.status], x1.value(), x2.value(),
      {n: c.pi for n, c in m.constraints.items()})
```
- `scipy.optimize.linprog(method="highs")` minimises only — negate to maximise; duals
  are in `res.ineqlin.marginals` (checked on this model with the negated objective: [-11.25, -2.5], so flip the sign to read them as profit per unit of resource; x = [20, 15], objective 1350).
- Excel Solver: choose "Simplex LP" and request the Sensitivity Report (gated: unconfirmed, source is paywalled or blocked).
Simplex and interior-point both solve LPs to optimality; interior-point is often faster
on very large sparse models, simplex gives a clean basis for sensitivity.

## 4. Read the dual (shadow prices)
The **dual value** of a constraint = change in optimal objective per unit increase in
its right-hand side, valid within its **allowable range**. In the example, solving the
dual gives wood = 11.25 and labour = 2.5 per unit: an extra hour of labour is worth
2.50 — pay no more than that for overtime. A non-binding constraint has dual value 0.
**Reduced cost** of a variable at zero = how much its objective coefficient must improve
before it enters the solution.
Signs depend on solver convention and min/max sense — sanity-check by re-solving with
RHS + 1.

## 5. Sensitivity and ranging
Ask for RHS ranges and objective-coefficient ranges (Excel report; Gurobi `SARHSLow/Up`,
`SAObjLow/Up`). Inside the range, the same basis stays optimal and duals stay valid.
Outside it, re-solve. For bigger "what-ifs", run scenarios — ranging is one-change-at-a-time.

## 6. When the solver says no
- **Infeasible:** constraints contradict. Find the conflict with an IIS (Gurobi
  `computeIIS()`) or add slack variables with a penalty cost and see which go positive.
  Usual culprits: wrong sign (≤ vs ≥), unit mismatch, demand above total capacity.
- **Unbounded:** a missing constraint or missing nonnegativity bound.
- **Degenerate / multiple optima:** several plans give the same objective; reported
  duals may not be unique. Add a secondary objective if the choice matters.

## Gotchas
- Fractional answers are legitimate in an LP; rounding them can break constraints —
  if integrality matters, model it.
- Huge differences in coefficient magnitude (1e-6 next to 1e6) cause numerical trouble;
  rescale units.
- Uncertain: PuLP's HiGHS integration name and availability depend on version; CBC is the safe default.

## Verify
- [ ] Every variable and constraint has units; all expressions linear.
- [ ] Solver status is Optimal, not just "a solution".
- [ ] Hand-check: plug the solution into each constraint.
- [ ] Binding constraints and their dual values explained in plain language.
- [ ] Key duals confirmed by re-solving with a perturbed RHS.
