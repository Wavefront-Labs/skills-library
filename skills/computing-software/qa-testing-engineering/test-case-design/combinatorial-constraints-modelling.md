---
id: computing-software.qa-testing-engineering.test-case-design.combinatorial-constraints-modelling
name: combinatorial-constraints-modelling
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [combinatorial-constraints, combinatorial-testing, invalid-combinations, constraint-modelling, pairwise-testing]
level: practitioner
status: docs-checked
description: "Model constraints in combinatorial test design: excluded and required combinations, conditional parameters, and avoiding lost pairs and over-constraining."
sources:
  - https://github.com/microsoft/pict/blob/main/doc/pict.md
  - https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constraints in combinatorial models

**Goal:** generated combinations are all executable, and constraints do not silently remove coverage you need. PICT constraint syntax (PICT documentation).

## Kinds of constraints
- **Impossible** (environment): a browser that is not available on every OS.
- **Business-invalid**: express shipping not offered for international; invoices only for business customers. Decide: exclude from the generated *valid* set, and test the rejection separately as negative tests.
- **Conditional parameters**: "card type" only relevant when payment = Card. Model with a "N/A" value and constraints:
  ```
  Payment: Card, PayPal
  CardType: Visa, Amex, NA
  IF [Payment] = "Card" THEN [CardType] <> "NA" ELSE [CardType] = "NA";
  ```

## Pitfalls
- **Over-constraining**: each constraint removes pairs; too many and the model barely tests interactions. Review whether a constraint reflects reality or an assumption.
- **Lost pairs**: a pair that is valid but cannot appear because of a chain of constraints. Check whether your generator reports pairs it could not cover, and review the count.
- Business-invalid combos excluded from generation never get a negative test unless you add one deliberately.

## Tools
PICT (`IF ... THEN ... ELSE ...` constraints; relations `=`, `<>`, `>`, `>=`, `<`, `<=`, `LIKE`). NIST ACTS is another combinatorial test generation tool (NIST project page).

## Verify
Every generated row executes successfully; excluded combinations are listed with reason and, where business-invalid, a separate negative test.

## Checked

2026-10-28 Confirmed against: PICT documentation (IF/THEN/ELSE constraint syntax and relations), NIST ACTS project page (tool exists). Removed or generalised: ACTS feature claims (constraint solver, GUI/CLI, invalid-combination reporting), allpairspy `filter_func`, Hexawise/TestDesigner, and the browser-OS example (not in the fetched pages).

Method: documentation only; no commands were run.
