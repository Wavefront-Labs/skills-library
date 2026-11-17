---
id: computing-software.qa-testing-engineering.test-case-design.identifying-equivalence-partitions-from-specs
name: identifying-equivalence-partitions-from-specs
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [partition-identification, equivalence-partitioning, black-box-testing, test-design, istqb]
level: practitioner
status: draft
description: "Identify equivalence partitions from a specification using the range, count, set and must-be heuristics, including invalid and hidden partitions."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identifying partitions from specifications

**Goal:** a complete, non-overlapping set of partitions per input or output before choosing values. CTFL v4.0 4.2.1.

## Heuristics (Myers, classic)
| Spec shape | Valid partitions | Invalid partitions |
|---|---|---|
| Range "1 to 99" | 1..99 | < 1, > 99, non-numeric |
| Count "1 to 6 owners" | 1..6 | 0, > 6 |
| Set "card is VISA, MC, AMEX" | each member if handled differently, else one | not in set, empty |
| Must-be "first char must be a letter" | letter | not a letter |
| Boolean / flag | true, false | missing / null |

## Procedure
1. List every input *and* output, including implicit ones (current date, user role, locale, system state).
2. For each, apply the heuristics; write partitions as a table with ID, rule, valid/invalid, source sentence.
3. Split a partition further if the spec or the code treats sub-ranges differently (e.g. tax bands, age 0-12, 13-17, 18+).
4. Add **type** partitions: wrong type, empty string, whitespace, null, too long, special characters.
5. Check: partitions are disjoint and cover the whole domain (every possible value belongs to exactly one).
6. Question gaps: the spec says 1-99 and 100+ but not 0; raise it.

## Example: discount code field
| ID | Partition | Type |
|---|---|---|
| P1 | 8 alphanumeric chars, active code | valid |
| P2 | 8 chars, expired code | invalid (business) |
| P3 | length < 8 | invalid |
| P4 | length > 8 | invalid |
| P5 | non-alphanumeric chars | invalid |
| P6 | empty | valid (no discount) per spec |

## Gotchas
- Partitions come from behaviour, not data type: two values are equivalent only if the system should treat them the same.
- Output partitions (error message types, discount tiers) reveal input partitions the spec forgot.
- One invalid partition per test, otherwise one error masks another.

## Verify
Each partition cites its source; the set is disjoint and complete; unclear areas are logged as questions.
