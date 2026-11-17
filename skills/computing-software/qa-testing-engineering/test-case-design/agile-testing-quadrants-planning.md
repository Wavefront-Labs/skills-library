---
id: computing-software.qa-testing-engineering.test-case-design.agile-testing-quadrants-planning
name: agile-testing-quadrants-planning
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [agile-testing-quadrants, test-strategy, test-planning, agile-testing, marick-quadrants]
level: practitioner
status: docs-checked
description: "Plan test coverage with the agile testing quadrants (Marick, Crispin/Gregory): classify tests, find missing quadrants, and assign tools and owners per quadrant."
sources:
  - https://lisacrispin.com/2011/11/08/using-the-agile-testing-quadrants/
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Planning with the agile testing quadrants

**Goal:** make sure a release's testing covers all four purposes, not just the ones the team is comfortable with.

## The quadrants
| | Supporting the team | Critiquing the product |
|---|---|---|
| **Business facing** | Q2: functional tests, examples, prototypes | Q3: exploratory, usability, UAT |
| **Technology facing** | Q1: unit and component tests | Q4: performance, load, security testing |

Numbering is not order; Q4 work sometimes needs to start first (for example a performance test on an architecture spike).

## Planning exercise (per release or epic)
1. Draw the grid on a whiteboard.
2. List planned testing activities as sticky notes; place each.
3. Look at empty or thin quadrants: why? (e.g. no Q4 for a feature with a peak-load risk).
4. For each note: tool, owner, when (sprint), automation yes/no, environment needed.
5. Keep the grid in the test strategy and revisit at release planning.

## Example (new checkout)
- Q1: pricing rules unit tests, repository integration tests.
- Q2: acceptance tests from example mapping; API contract tests.
- Q3: exploratory charters on payment errors; usability session with 5 shoppers.
- Q4: load test above expected peak, security scan, failover test of payment provider.

## Gotchas
- Treating Q3 as optional "if time allows"; it finds what the specs missed.
- Q4 left to the end of the release; performance problems found late are architectural.

## Verify
Every quadrant has at least one planned activity with an owner for each significant feature, or an explicit reason why not.

## Checked

2026-10-28. Confirmed: Crispin quadrants article: numbering implies no order; Q2 examples and prototypes; Q3 exploratory, usability, UAT; Q4 performance, security and load; a project may start Q4 with a performance test on an architecture spike. Removed: Syllabus section number, simulations, alpha/beta, reliability items and named tools (Testcontainers, Gherkin, k6, ZAP).

Method: documentation only; no commands were run.
