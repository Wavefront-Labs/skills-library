---
id: computing-software.qa-testing-engineering.test-case-design.atdd-acceptance-test-workshops
name: atdd-acceptance-test-workshops
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [atdd, acceptance-test-driven-development, specification-workshop, test-first, specification-by-example, acceptance-tests, istqb]
level: practitioner
status: draft
description: "Run ATDD: a specification workshop turns a story into concrete examples, which become automated acceptance tests written before the code and run in CI."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://gojko.net/books/specification-by-example/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ATDD: acceptance test workshops

**Goal:** agree what "done" means with concrete examples before coding, then automate those examples. ISTQB CTFL v4.0 4.5.3; Adzic, *Specification by Example*.

## Workshop (30-60 min per story)
1. Product owner explains the story and its business rule.
2. Group (business, dev, tester) writes **examples**: inputs and expected outcomes, including boundaries and failure cases.
3. Spot rules hidden in examples; split the story if examples reveal several rules.
4. Record open questions; do not start a story with unresolved ones.

## From examples to tests
- Order of examples: positive happy path, then negative, then non-functional (e.g. response time).
- Write them in the team's chosen form: Gherkin (`gherkin-given-when-then-scenarios`), a table-driven test, or Robot Framework keywords.
- Automate at the lowest level that can exercise the rule (often API/service level, not UI).
- Tests start red; the story is done when they are green in CI.

## Example table
| Basket total | Customer type | Discount |
|---|---|---|
| 99.99 | standard | 0% |
| 100.00 | standard | 5% |
| 100.00 | gold | 10% |
| 0 | gold | 0% |

## Gotchas
- Examples that describe UI clicks instead of business rules are brittle; describe the rule.
- ATDD without the business participant is just test automation written early.

## Verify
Every story in progress has examples agreed before the first commit, and the acceptance tests failed before implementation.
