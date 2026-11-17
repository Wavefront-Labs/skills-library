---
id: computing-software.qa-testing-engineering.test-case-design.extended-entry-decision-tables
name: extended-entry-decision-tables
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [extended-entry-decision-table, decision-tables, multi-valued-conditions, business-rules-testing, istqb]
level: practitioner
status: draft
description: "Use extended-entry decision tables when conditions have more than two values (ranges, categories), combining them with equivalence partitions and boundaries."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extended-entry decision tables

**Goal:** model rules whose conditions are multi-valued (ranges, categories) without blowing up into Boolean conditions. ISTQB CTFL v4.0 4.2.3 (limited-entry vs extended-entry).

## Shape
Each condition row takes values from a partition list instead of T/F.

| Condition | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Customer tier | bronze | silver | gold | gold | - |
| Basket total | < 50 | >= 50 | < 100 | >= 100 | - |
| Region | domestic | domestic | domestic | domestic | international |
| **Shipping** | 4.99 | free | 2.99 | free | 19.99 |

Number of full combinations = product of partition counts; collapse with `-` like Boolean tables (`collapsing-decision-tables`).

## Deriving tests
1. One test per rule (column).
2. Pick representative values within each partition, then add **boundary values** where partitions are ranges (49.99 / 50.00 for R1/R2), combining with BVA.
3. Add invalid partitions separately (unknown tier, negative total).

## When to use
Pricing, eligibility, insurance rating, tax and shipping rules: business rules with categorical or ranged inputs.

## Gotchas
- Partitions must be non-overlapping and complete per condition; gaps (what about exactly 100 for silver?) surface spec defects.
- Very large tables signal a need for a rules engine test harness, data-driven tests (`decision-table-as-parametrized-tests`).

## Verify
Each condition's partitions cover its whole domain, every feasible column is covered by a test, and range edges have boundary tests.
