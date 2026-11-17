---
id: computing-software.qa-testing-engineering.test-case-design.classification-tree-method
name: classification-tree-method
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [classification-tree-method, combinatorial-testing, cte, test-design-techniques, istqb-ta]
level: practitioner
status: docs-checked
description: "Design tests with the classification tree method: aspects as classifications, partitions as classes, then mark combinations in the table below the tree."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
  - https://www.razorcat.com/en/product-cte.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Classification tree method

**Goal:** a visual, reviewable way to partition test-relevant aspects and pick combinations. Razorcat's CTE page describes the method.

## Build the tree
1. Root: the test object (e.g. "Flight search").
2. **Classifications**: test-relevant aspects (trip type, passengers, cabin, date range, flexibility).
3. **Classes**: disjoint, complete partitions of each classification (trip type: one-way | return | multi-city). Classes can be refined into sub-classifications (passengers -> adults 1 | 2-9; children 0 | 1+; infants 0 | 1+ with "infants <= adults").
4. Draw it (Razorcat's Classification Tree Editor CTE, or a mind map/spreadsheet).

## Combination table
Under the tree, each row is a test case; mark one class per classification. Strategy:
- Minimal: each class at least once (each choice).
- Pairwise between selected classifications (if your tool supports it).
- Add rows for specific risky combinations.
Plus constraints/dependency rules (multi-city only for economy? infants need an adult).

## Strengths
- Shows coverage gaps visually; easy review with domain experts.
- Combines EP (classes) with combinatorial selection.

## Gotchas
- Classes must not overlap and must cover the domain; boundary values still need BVA within classes.
- Large trees: split by sub-feature.

## Verify
Every class is marked in at least one row; dependency rules are honoured; domain expert reviewed the tree.

## Checked

2026-10-28 Confirmed against: Razorcat CTE page (classification tree method, combination table below the tree, test cases from marking classes). Removed or generalised: the original-authors attribution, the ISTQB section number, and the TESTONA/CTE XL tool names (not in the fetched pages).

Method: documentation only; no commands were run.
