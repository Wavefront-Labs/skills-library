---
id: computing-software.qa-testing-engineering.test-case-design.decision-trees-vs-decision-tables
name: decision-trees-vs-decision-tables
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [decision-tree-testing, decision-table-testing, classification-tree, business-rules, test-design]
level: practitioner
status: draft
description: "Choose decision trees over tables for nested, ordered rules, derive one test per root-to-leaf path, and convert between trees and tables."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Decision trees vs tables for nested rules

**Goal:** model rules in the form that fits their structure and test them completely.

## When a tree fits better
- Conditions are evaluated in a fixed order and later conditions only matter on some branches ("if not a customer, nothing else matters").
- Conditions have many values (country, product type) that would explode a table.
- Stakeholders already think in flowcharts.
A table fits better for independent conditions with all combinations relevant.

## Example: loan pre-approval
```text
Existing customer?
|-- no  -> Age >= 18? -- no -> reject
|                      -- yes -> credit score >= 650? -- no -> reject / -- yes -> refer
|-- yes -> Arrears in 12 months? -- yes -> reject
                                 -- no  -> amount <= 3x income? -- yes -> approve / -- no -> refer
```
Leaves: 6 paths -> 6 test cases (one per root-to-leaf path), versus 2^5 = 32 rows in a full table, most of them don't-care.

## Coverage
- **Leaf (path) coverage:** every root-to-leaf path exercised; the natural target.
- **Branch coverage of the tree:** every edge exercised (implied by leaf coverage).
- Add BVA on numeric splits (649/650, exactly 3x income).

## Converting
Each root-to-leaf path is one collapsed table column: conditions on the path get values, all others "-". Use this to check the tree for completeness with table tools.

## Gotchas
- Order matters: the implementation may evaluate in a different order; when conditions have side effects or short-circuit, test that the order matches.
- Missing else-branches are common in trees drawn from prose; every split needs every outcome.
- For ML decision trees, this technique does not apply; test them with data-based methods.

## Verify
Every leaf has a test, every numeric split has boundary tests, and the tree was reviewed with the rule owner.
