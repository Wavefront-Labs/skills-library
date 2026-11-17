---
id: computing-software.qa-testing-engineering.test-automation.testing-dmn-and-rules-engine-decision-tables
name: testing-dmn-and-rules-engine-decision-tables
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [dmn-testing, rules-engine-testing, decision-table-testing, camunda, drools]
level: practitioner
status: draft
description: "Test DMN and rules-engine decision tables: hit policies, FEEL expressions, gap/overlap analysis, table-driven unit tests and rule versioning."
sources:
  - https://www.omg.org/dmn/
  - https://docs.camunda.io/docs/components/modeler/dmn/decision-table-hit-policy/
  - https://www.drools.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing DMN and rules-engine decision tables

**Goal:** business-editable rules need the same rigour as code, because business users change them without a developer.

## Know the hit policy (DMN 1.x)
| Policy | Meaning | Test focus |
|---|---|---|
| U Unique | exactly one rule may match | overlaps are errors; test overlapping inputs fail validation |
| A Any | several may match if outputs equal | conflicting outputs |
| P Priority | highest-priority output wins | priority order |
| F First | first matching rule in order | order of rows matters; test that reordering is caught |
| C Collect (+ sum/min/max/count) | all matches aggregated | aggregation result |
| R Rule order / O Output order | list of outputs | sequence |

## Test design
1. Treat the table as a decision table: one test per rule (decision table coverage), BVA on every FEEL range (`[18..65]` inclusive vs `(18..65)` exclusive, `< 100`).
2. Gap test: inputs matching no rule -> what is the default/null output? Specify it.
3. Overlap test for Unique policy: tooling (Camunda Modeler, Drools DMN validation) flags overlaps; also assert in tests.
4. Null/missing input handling: FEEL comparisons with null yield null, often matching nothing.

## Table-driven unit tests (Camunda 7 DMN engine example)
```java
DmnEngine engine = DmnEngineConfiguration.createDefaultDmnEngineConfiguration().buildEngine();
DmnDecision d = engine.parseDecision("discount", getClass().getResourceAsStream("/discount.dmn"));

@ParameterizedTest
@CsvSource({ "gold,99.99,0.05", "gold,100,0.10", "silver,100,0.05" })
void discount(String tier, double total, double expected) {
  DmnDecisionTableResult r = engine.evaluateDecisionTable(d,
      Variables.createVariables().putValue("tier", tier).putValue("total", total));
  assertEquals(expected, (double) r.getSingleResult().getEntry("rate"), 1e-9);
}
```
Drools/Kogito: evaluate via `DMNRuntime.evaluateAll(model, context)` and assert `DMNResult` with no messages of severity ERROR. Kogito also supports scenario simulation (`.scesim`) files business users can edit.

## Process
- Rules versioned in Git; every change goes through the table-driven test suite in CI.
- Business owner adds an example row to the test CSV with each rule change.

## Gotchas
- String inputs are case-sensitive in FEEL; `"Gold"` matches nothing.
- Floating comparisons at boundaries: use decimal types where money is involved.

## Verify
Every rule row has a test, FEEL range boundaries are tested on both sides, and gap/overlap analysis is clean or documented.
