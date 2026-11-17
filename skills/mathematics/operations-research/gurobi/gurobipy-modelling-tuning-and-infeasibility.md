---
id: mathematics.operations-research.gurobi.gurobipy-modelling-tuning-and-infeasibility
name: gurobipy-modelling-tuning-and-infeasibility
category: mathematics
field: operations-research
product: gurobi
tags: [operations-research, gurobi, gurobipy, solver, mip, lp, qp, optimisation, optimization, addvars, addconstrs, quicksum, tupledict, model-status, mipgap, timelimit, mipfocus, presolve, tuning-tool, computeiis, iis, feasrelax, infeasibility, numerical-issues, warm-start, solution-pool, gurobi-log, license]
level: practitioner
status: docs-checked
description: "Use gurobipy: build with addVars/addConstrs, check status codes, set MIPGap/TimeLimit/MIPFocus, tune, and diagnose infeasibility with IIS."
sources: ["https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html", "https://docs.gurobi.com/projects/optimizer/en/current/reference/python/model.html", "https://docs.gurobi.com/projects/optimizer/en/current/reference/python/tupledict.html", "https://docs.gurobi.com/projects/optimizer/en/current/reference/numericcodes/statuscodes.html", "https://docs.gurobi.com/projects/optimizer/en/current/reference/attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gurobipy: modelling, tuning and infeasibility

**Goal:** build an optimisation model in Gurobi's Python API that is readable, solves
within your time budget, and fails informatively when the data are wrong.

## 1. Build models in bulk
```python
import gurobipy as gp
from gurobipy import GRB
with gp.Env() as env, gp.Model("assign", env=env) as m:
    x = m.addVars(workers, tasks, vtype=GRB.BINARY, name="x")   # tupledict keyed (w, t)
    m.addConstrs((x.sum("*", t) == 1 for t in tasks), name="cover")
    m.addConstrs((x.prod(hours, w, "*") <= cap[w] for w in workers), name="cap")
    m.setObjective(x.prod(cost), GRB.MINIMIZE)   # hours, cost: dicts keyed (w, t)
    m.Params.TimeLimit = 120
    m.Params.MIPGap = 0.01
    m.optimize()
```
- `addVars` returns a **tupledict** whose keys come from the index arguments; `x.sum(...)`
  and `x.prod(coeff, ...)` build linear expressions over a pattern (`"*"` is a wildcard).
- **Name everything**: names appear in IIS output and in files written with `m.write(...)`.
- For NumPy-heavy models there is a matrix API (`addMVar`).
- The Gurobi documentation examples create the environment and model inside `with`
  blocks (context managers) so they are disposed of when the block ends.

## 2. Check status before reading values
```python
if m.Status == GRB.OPTIMAL: ...
elif m.Status == GRB.TIME_LIMIT and m.SolCount > 0: ...   # time ran out; a solution exists
elif m.Status == GRB.INFEASIBLE: ...
elif m.Status == GRB.INF_OR_UNBD: ...                     # infeasible or unbounded, undecided
```
- `OPTIMAL` (2): solved to optimality subject to tolerances. `INFEASIBLE` (3): proven
  infeasible. `INF_OR_UNBD` (4): infeasible or unbounded; the status docs say to set
  `DualReductions` to 0 and re-optimise for a definitive answer. `TIME_LIMIT` (9): the
  `TimeLimit` parameter was exceeded. `SUBOPTIMAL` (13): optimality tolerances could not be
  met but a sub-optimal solution is available.
- Attributes: solution values `x[w, t].X`, objective `m.ObjVal`, best bound `m.ObjBound`,
  relative gap `m.MIPGap`, solution count `m.SolCount`.
- The docs recommend comparing against the predefined status constants, not raw integers.

## 3. Parameters that matter most
| Parameter | What the Gurobi reference says |
|---|---|
| `TimeLimit` | Seconds; default Infinity; returns `TIME_LIMIT`. Runtime may overshoot slightly |
| `MIPGap` | Relative gap |z_P - z_D| / |z_P|; default 1e-4; solver stops when gap is below it |
| `MIPFocus` | Default 0 balances; 1 = find feasible solutions quickly; 2 = focus on proving optimality; 3 = focus on the bound when it is moving slowly |
| `Threads` | Default 0 = automatic (generally all virtual processors); lower it when sharing a machine |
| `Seed` | Default 0; a small perturbation that typically leads to different solution paths |
| `NumericFocus` | 0-3, default 0; higher values spend more time on numerical care |
| `Method` | Continuous models / MIP root: -1 automatic (default), 0 primal simplex, 1 dual simplex, 2 barrier, 3 concurrent, 4 deterministic concurrent |
`MIPFocus` only affects MIP models. Time limit and gap are business stopping rules; set
both.

**Tuning:** `m.tune()` searches for parameter settings that improve performance and stores
the best sets (count in the `TuneResultCount` attribute; read with `getTuneResult`).
Because a seed change alone alters solution paths, validate any tuned settings on other
instances and seeds, not only the one tuned.
**Warm start:** the `Start` variable attribute exists for supplying a starting solution.

## 4. Diagnose infeasibility
```python
m.computeIIS()
m.write("model.ilp")      # write the IIS to a file (the suffix selects the format)
for c in m.getConstrs():
    if c.IISConstr: print(c.ConstrName)
```
`computeIIS` finds an Irreducible Inconsistent Subsystem: a subset of constraints and
variable bounds that is infeasible together. Read the constraints it names first.
If the business wants the least-violating plan instead, `m.feasRelaxS(relaxobjtype,
minrelax, vrelax, crelax)` builds a feasibility relaxation, e.g.
`m.feasRelaxS(0, False, False, True)`: `relaxobjtype=0` minimises the sum of violation
magnitudes (1 = sum of squares, 2 = number of violations); `crelax=True` lets constraints
be relaxed, `vrelax=False` keeps variable bounds. It modifies the model in place (use
`m.copy()` first to keep the original), and you must call `optimize()` on the result.

## 5. Other points from the reference
- `addGenConstrIndicator` adds an indicator constraint (binary variable, value, then a
  linear constraint); consider it instead of a hand-rolled big-M.
- After changing a model, `m.update()` processes pending modifications; `optimize()` and
  `write()` also process them.
- `PoolSearchMode = 2` with `PoolSolutions = n` finds the n best solutions (default
  `PoolSolutions` is 10); read alternatives with `SolutionNumber` and the `Xn` attribute.
  Larger values cost more solve time.

## Gotchas
- `TIME_LIMIT` with `SolCount` = 0 means no plan at all; have a fallback heuristic.
- Check licence terms for your deployment (academic, size-limited and production
  licences differ); see Gurobi's licensing documentation.

## Verify
- [ ] Status checked before reading values.
- [ ] `TimeLimit` and `MIPGap` set to business-agreed values.
- [ ] Infeasible cases produce an IIS naming the conflicting constraints.
- [ ] Tuned parameters validated across several instances and seeds.

## Checked
2026-11-09. Confirmed against the Gurobi Optimizer reference pages listed in sources:
parameter defaults and meanings (TimeLimit, MIPGap, MIPFocus, Threads, Seed, NumericFocus,
Method, DualReductions, PoolSearchMode, PoolSolutions), status codes and their numbers,
`feasRelaxS` arguments and behaviour, `computeIIS`, `tune`, `update`, `write`, tupledict
`sum`/`prod`/`select`, `addGenConstrIndicator`, `addMVar`, and attribute names (X, ObjVal,
ObjBound, MIPGap, SolCount, Start, IISConstr, ConstrName, Xn). Removed: coefficient-range
thresholds, presolve and root-gap log interpretation, the `x.X > 0.5` rule, the claim that
`+=` loops are much slower, `quicksum` usage, big-M magnitudes, and licence size details,
none of which were stated on the pages read. Partial read: the attributes page was a name
list only, so attribute semantics beyond names rest on the Model method pages.
Method: documentation only; no commands were run.
