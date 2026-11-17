---
id: computing-software.qa-testing-engineering.test-case-design.open-and-undefined-boundaries
name: open-and-undefined-boundaries
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [open-boundaries, boundary-value-analysis, undefined-boundaries, black-box-testing, requirements-clarification]
level: practitioner
status: draft
description: "Handle open-ended and undefined boundaries in BVA: pick values from storage limits, related specs and risk, and get the missing boundary specified."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open-ended and undefined boundaries

**Goal:** test sensibly when the spec gives only one side of a range ("18 and over", "at least 1 item") or none at all.

## Finding the missing boundary
1. **Ask** the product owner: "What is the maximum order quantity?" An unknown boundary is a requirements defect; log it.
2. **Look at implementation limits:** column type (`VARCHAR(255)`, `SMALLINT` 32767, `INT` 2,147,483,647), API schema `maximum`, language integer size, UI `maxlength`.
3. **Look at related specs and business sense:** age > 130 is not credible; order quantity above warehouse stock; payment above card limits.
4. **Look at other systems** that consume the value (a downstream system with a smaller field truncates).

## Choosing test values
| Situation | Values |
|---|---|
| Lower bound only (>= 18) | 17, 18 and a large realistic value; then the storage max and max+1 |
| No bound defined | typical value, zero, negative, very large (storage max), max+1, extremely long input |
| Open boundary on a real number (> 0) | 0, smallest representable positive at the stored precision (0.01 for money) |

## Expected results
Where nothing is specified, the minimum expectation is graceful handling: validation error, no crash, no truncation without warning, no overflow wrapping to negative.

## Example
"Discount applies to orders of 100.00 or more." Test 99.99, 100.00, and also 99,999,999.99 (column max for `DECIMAL(10,2)`) and 100,000,000.00 (overflow) to see how the API reacts.

## Gotchas
- Integer overflow at hidden limits is a classic security and data-integrity bug.
- UI may allow values the DB rejects, giving 500 errors; test through the full stack.
- Record the boundary you assumed in the test case so it is revisited when the spec is fixed.

## Verify
Each open boundary has either a specified value from the product owner or a documented assumption with its source (schema, column type).
