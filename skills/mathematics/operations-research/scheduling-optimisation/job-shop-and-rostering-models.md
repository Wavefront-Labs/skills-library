---
id: mathematics.operations-research.scheduling-optimisation.job-shop-and-rostering-models
name: job-shop-and-rostering-models
category: mathematics
field: operations-research
product: scheduling-optimisation
tags: [operations-research, scheduling-optimisation, scheduling, job-shop-scheduling, flow-shop, makespan, tardiness, dispatching-rules, spt, edd, constraint-programming, cp-sat, or-tools, interval-variables, no-overlap, cumulative-constraint, rostering, nurse-rostering, shift-scheduling, timetabling, vehicle-routing, vrp, hard-constraints, soft-constraints, local-search]
level: advanced
status: docs-checked
description: "Model scheduling and rostering: pick the objective, dispatching rules vs CP-SAT vs MIP, encode no-overlap and shift rules, separate hard from soft constraints, validate."
sources: ["https://developers.google.com/optimization/scheduling/job_shop", "https://developers.google.com/optimization/cp/cp_example"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job-shop and rostering models

**Goal:** turn "who/what does which task when" into a model that a solver can handle
and planners will accept.

## 1. Classify the problem
| Type | Decisions | Typical objective |
|---|---|---|
| Single machine | job order | total tardiness, max lateness |
| Flow shop | same route for all jobs | makespan |
| Job shop | each job has its own machine route | makespan, weighted tardiness |
| Shift / rostering | which person works which shift | cover demand, fairness, preferences |
| Timetabling | events to rooms × times | no clashes, compactness |
| Vehicle routing | stops to vehicles and order | distance, vehicles used, time windows |
Most are NP-hard: aim for good solutions with bounds, not guaranteed optima at scale.

## 2. Pick the objective carefully
- **Makespan** (finish everything ASAP) vs **total weighted tardiness** (customers'
  due dates) vs **flow time** (WIP). They give very different schedules.
- Combine objectives lexicographically (meet hard due dates first, then minimise
  overtime) rather than with arbitrary weights where possible.

## 3. Quick baselines: dispatching rules
Always compute a rule-based schedule first — it's a feasible benchmark.
- **SPT** (shortest processing time first) minimises average flow time on one machine.
- **EDD** (earliest due date) minimises maximum lateness on one machine.
- **Johnson's rule** gives the optimal makespan for a two-machine flow shop.
In job shops, rules are heuristics; use them as starting solutions.

## 4. Constraint programming with OR-Tools CP-SAT
OR-Tools CP-SAT has interval variables and no-overlap constraints for scheduling:
```python
from ortools.sat.python import cp_model
m = cp_model.CpModel(); H = sum(d for job in jobs for _, d in job)   # horizon
ends, per_machine = [], {}
for j, job in enumerate(jobs):                 # job = [(machine, duration), ...]
    prev_end = None
    for k, (mach, dur) in enumerate(job):
        s = m.NewIntVar(0, H, f"s{j}{k}"); e = m.NewIntVar(0, H, f"e{j}{k}")
        iv = m.NewIntervalVar(s, dur, e, f"i{j}{k}")
        per_machine.setdefault(mach, []).append(iv)
        if prev_end is not None: m.Add(s >= prev_end)   # precedence within job
        prev_end = e
    ends.append(prev_end)
for ivs in per_machine.values(): m.AddNoOverlap(ivs)
mk = m.NewIntVar(0, H, "makespan"); m.AddMaxEquality(mk, ends); m.Minimize(mk)
solver = cp_model.CpSolver(); solver.parameters.max_time_in_seconds = 60
solver.parameters.num_workers = 8; status = solver.Solve(m)
```
- `AddCumulative` for resources with capacity > 1 (a crew of 3).
- Optional intervals (`NewOptionalIntervalVar`) for "which machine" choices.
- Integer time units: pick a granularity (5 min) — finer grains slow solving.
Time-indexed MIPs (x_{j,t} = 1 if job j starts at t) grow with the horizon.

## 5. Rostering: hard vs soft constraints
Variables: x[p, d, s] = 1 if person p works shift s on day d.
- **Hard:** cover minimums per shift, ≤ 1 shift per day, minimum rest between shifts
  (forbid late → early next day), legal max hours, qualifications.
- **Soft (penalised):** preferences, fairness of weekends/nights, consecutive-day limits.
  Model as slack variables with weights; report each penalty term separately so planners
  see the trade-offs.
Fairness: minimise the max (or the spread) of nights per person, not just the total.
Check labour rules for your jurisdiction — they vary; the model is only as legal as its inputs.

## 6. Routing
Use a specialised routing solver (for example the OR-Tools routing library) rather than
a hand-written MIP. Supply a
travel-time matrix that reflects real roads and time of day.

## 7. Validate and deploy
- Write an **independent checker** that verifies every hard constraint on the output.
- Visualise as a **Gantt chart** (per machine/person) — planners spot nonsense instantly.
- Expect disruptions: design for **rescheduling** with minimal change (penalise moves
  from the published schedule).

## Gotchas
- An unrealistically tight horizon makes the model infeasible; a loose one slows it.
- Forgetting setup/changeover times (sequence-dependent) makes schedules unachievable.
- Optimising averages can starve individual jobs or people — check the worst case.
- CP-SAT has both CamelCase and snake_case method names in current releases; match your installed version.

## Checked
2026-11-01. The CP-SAT code uses methods that exist in the installed OR-Tools (NewIntervalVar, NewOptionalIntervalVar, AddNoOverlap, AddCumulative, AddMaxEquality, solver parameters max_time_in_seconds and num_workers) and matches the OR-Tools job-shop guide. SPT (average flow time), EDD (maximum lateness) and Johnson's rule (two-machine flow-shop makespan) were verified by brute force over 300 random 6-job instances with a short Python script. Removed: the claim CP-SAT is the strongest free tool and the VROOM mention.

Method: documentation plus short Python computations; the skill's own commands were not run.

## Verify
- [ ] Problem type and single primary objective stated.
- [ ] Dispatching-rule baseline computed and beaten (or matched with justification).
- [ ] Independent checker passes all hard constraints.
- [ ] Soft-constraint penalties reported individually.
- [ ] Gantt view reviewed by someone who runs the operation.
