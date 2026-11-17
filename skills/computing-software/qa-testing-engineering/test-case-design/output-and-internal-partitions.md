---
id: computing-software.qa-testing-engineering.test-case-design.output-and-internal-partitions
name: output-and-internal-partitions
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [output-partitioning, equivalence-partitioning, output-based-testing, internal-partitions, black-box-testing]
level: practitioner
status: draft
description: "Partition outputs and internal values, not just inputs: derive tests that drive each distinct output class, message, state or computed range."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Output and internal partitions

**Goal:** make sure every distinct *result* the system can produce is exercised. ISTQB CTFL v4.0 4.2.1 (partitions can apply to outputs, internal values, time-related values and interface parameters).

## Procedure
1. List the outputs and their classes from the spec: messages, statuses, categories, computed ranges, files produced, side effects.
   Example, loan decision: `approved`, `approved with conditions`, `referred to underwriter`, `declined (credit score)`, `declined (affordability)`.
2. For each output partition, work backwards to inputs that produce it.
3. Also partition **internal values** that drive behaviour: computed risk score bands, intermediate totals that cross thresholds, retry counters, cache hit vs miss, queue length.
4. Combine with input partitions: tests should cover both sets.

## Example
Shipping cost output bands: free (basket >= 50), standard 4.99, heavy-item surcharge, international. Input partitioning on basket total alone misses the heavy-item band reached by item weight.

## Why it matters
Input partitions can all be covered while an output (e.g. a rare error message, a specific report section) is never produced. Output-driven tests find unreachable or wrongly-reached outputs.

## Gotchas
- Outputs that need hard-to-create states (referred to underwriter) often go untested; use test hooks or seeded data.
- Error outputs from dependencies (timeouts) are partitions too.

## Verify
A list of all output classes, each with at least one test that produced it, verified in the result (not assumed).
