---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.stateflow-chart-coverage-testing
name: stateflow-chart-coverage-testing
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [stateflow-coverage, model-coverage, simulink-coverage, test-cases, mcdc, simulink-test]
level: practitioner
status: gated
description: "Drive Stateflow charts to structural coverage with Simulink Test cases, read the coverage report, and justify unreachable or untestable objectives."
sources:
  - "Simulink Coverage and Simulink Test documentation (mathworks.com)"
  - "ISO 26262 part 6 coverage guidance; confirm the edition and ASIL expectations"
  - "https://www.mathworks.com/help/slcoverage/ug/types-of-model-coverage.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Stateflow chart coverage testing

1. Enable coverage in the test manager (Simulink Coverage reports decision coverage on Stateflow states, and condition and MC/DC on transitions, plus cyclomatic complexity and relational boundary; choose per project. ISO 26262-6 recommends structural coverage metrics by ASIL (gated: unconfirmed, source is paywalled or blocked); confirm the table in the current edition).
2. Write requirements-based test cases first (inputs timelines via signal editor), then run and read the report to find gaps.
3. For uncovered transitions: decide whether the missing case is a missing requirement test or truly dead logic. Dead logic is removed or justified in writing, not covered with a contrived test.
4. MC/DC for compound conditions: tabulate independent-effect pairs.
5. Save the model coverage data with the model version for the audit trail; rerun after any chart edit.
6. Coverage proves test thoroughness, not correctness; keep requirement-based checks (assessments) in each test.

**Gotchas:** coverage achieved at model level is not code-level coverage; for code, use a code coverage tool on the generated code if required.

## Verify
- [ ] Coverage report shows target percentage with every gap justified.
- [ ] Each test case links to a requirement.
