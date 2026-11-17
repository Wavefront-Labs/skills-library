---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.stateflow-mode-manager-chart
name: stateflow-mode-manager-chart
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [stateflow, mode-manager, state-machine, supervisory-control, chart-structure, simulink]
level: practitioner
status: gated
description: "Structure a supervisory mode manager in Stateflow with exclusive states, explicit transitions, outputs set once per state, and testable inputs."
sources:
  - "Stateflow documentation (mathworks.com)"
  - "MathWorks Simulink modelling guidelines (confirm current edition)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Mode manager chart structure

1. Define modes as exclusive (OR) states: e.g. `Off`, `Ready`, `Drive`, `Fault`. Parallel (AND) states only for independent concerns (mode vs diagnostics).
2. Keep inputs as booleans/enums with clear names; avoid raw analogue thresholds in transitions (do that upstream in Simulink).
3. Outputs assigned in `entry:` or `during:` actions, and have a defined default so no output is left stale.
4. Make transition evaluation order explicit (chart property "User-specified state/transition execution order", reported enabled by default in current releases; gated: unconfirmed, source is paywalled or blocked) so evaluation is deterministic; avoid overlapping conditions.
5. Use enumerated types for state outputs to the rest of the model.
6. Add a top-level default transition and a `Fault` state reachable from anywhere (use a super-transition from the parent).

**Gotchas:** implicit event broadcasting; graphical function side effects; reaching unreachable states silently.

## Verify
- [ ] Model Advisor and Stateflow checks report no unreachable states or dead transitions.
- [ ] Each state and transition covered by at least one test.
