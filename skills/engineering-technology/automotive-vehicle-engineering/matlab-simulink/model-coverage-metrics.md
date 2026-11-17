---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.model-coverage-metrics
name: model-coverage-metrics
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [model-coverage, decision-coverage, condition-coverage, mcdc-coverage, lookup-coverage, coverage-gaps]
level: practitioner
status: gated
description: "Choose and interpret decision, condition, MC/DC and lookup-table coverage metrics for controllers, and decide what to do with uncovered objectives."
sources:
  - "Simulink Coverage: model coverage types (https://www.mathworks.com/help/slcoverage/ug/types-of-model-coverage.html)"
  - "ISO 26262 part 6; confirm edition and ASIL tables (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Model coverage metrics

- **Decision:** each branch outcome taken. **Condition:** each atomic condition both true and false. **MC/DC:** each condition independently affects the decision outcome (Simulink Coverage: full MCDC does not by itself imply full decision or condition coverage). **Lookup table coverage:** each interpolation interval exercised.
- Choose metrics by integrity level and project policy; higher ASILs ask for stronger structural coverage (check the current ISO 26262-6 table (gated: unconfirmed, source is paywalled or blocked)).
- Process: run requirement-based tests -> collect -> list uncovered objectives -> classify: missing test, dead logic, defensive code, unreachable by design.
- Justify unreachable objectives with analysis; remove truly dead logic.
- Combine results across test suites (merge coverage data) and keep the per-model report.
- Report both achieved percent and the list of justified objectives.

**Gotchas:** inflating coverage with tests that do not assert behaviour; saturation blocks counted as decisions.

## Verify
- [ ] Merged coverage meets the policy target.
- [ ] Every uncovered objective has a documented classification.
