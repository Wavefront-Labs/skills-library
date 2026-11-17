---
id: computing-software.software-engineering.prolog.clpfd-optimisation
name: clpfd-optimisation
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, clpfd-optimisation, labeling-options]
level: advanced
status: draft
description: "Optimise with labeling([min(E)]) / max(E), choose ff/ffc/leftmost/up/down/bisect, and time propagation."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Optimising and tuning search
```prolog
?- X in 0..10, Y in 0..10, X + 2*Y #=< 14, Z #= 3*X + 2*Y,
   labeling([max(Z)], [X,Y]).           % first solution is optimal, more on backtrack, non-increasing
?- length(Qs, 20), Qs ins 1..20, labeling([ff, bisect], Qs).
```
- Variable selection: `leftmost`, `ff`, `ffc`, `min`, `max`. Value order: `up`, `down`. Branching: `step`, `enum`, `bisect`.
- `labeling([min(Cost)], Vars)` enumerates solutions in increasing Cost, so take `once/1` for the optimum.
- Tune with `statistics(cputime, T)` around the call.
## Gotchas
- Optimisation labeling does not prune with bound updates like a MIP solver; add redundant constraints (`sum/3`) to prune.
- Large domains and non-linear constraints blow up: introduce intermediate variables.
## Self-check
Maximise a knapsack objective, then add a symmetric-breaking constraint and compare time.
