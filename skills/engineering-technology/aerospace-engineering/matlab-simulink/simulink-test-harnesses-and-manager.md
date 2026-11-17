---
id: engineering-technology.aerospace-engineering.matlab-simulink.simulink-test-harnesses-and-manager
name: simulink-test-harnesses-and-manager
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, model-based-verification, simulink-test, test-harness, test-manager, baseline-test, equivalence-test, regression]
level: practitioner
status: docs-checked
description: "Build Simulink Test harnesses and Test Manager suites with baseline, equivalence and assessment tests, and run them from scripts for continuous integration."
sources:
  - "https://www.mathworks.com/help/sltest/ref/sltest.harness.create.html"
  - "https://www.mathworks.com/help/sltest/ref/sltest.testmanager.run.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Simulink Test harnesses and Test Manager

**Goal:** repeatable model tests.

## Steps
1. Create a harness around a component: `sltest.harness.create('model/Controller', Name='ctrl_harness')`; the harness isolates the unit with its own inputs and sinks.
2. Test Manager: create a test file and test case (baseline, equivalence (back-to-back, for example model vs SIL), or simulation), choose inputs (signal editor, test sequence) and criteria (baseline, assessments with verify statements).
3. Run from script: `resultObj = sltest.testmanager.run` runs all test files loaded in the Test Manager and returns a `sltest.testmanager.ResultSet`; `sltest.testmanager.run(Name=Value)` restricts the run. Look up result export in the Simulink Test documentation.
4. Add to continuous integration so tests run on every change.

## Practice
- One harness per component with documented inputs; use Test Sequence blocks for scenario logic (step, ramp, fault injection).
- Keep baseline data under version control with the tolerance stated.
- Use equivalence tests between model and generated code (SIL) to demonstrate translation correctness.

## Gotchas
- Baselines that change with solver settings: pin solver and step.
- Tolerances too tight produce flaky tests.

## Verify
- [ ] Tests fail when a deliberate bug is injected into the unit.

## Checked
2026-11-01. Confirmed on the MathWorks pages: `sltest.harness.create(harnessOwner, Name=Value)` with Name as the harness name; `sltest.testmanager.run` syntax and its ResultSet output. Removed: `getResultSets` and `report` function names (not on the page read).
Method: documentation only; no commands were run.
