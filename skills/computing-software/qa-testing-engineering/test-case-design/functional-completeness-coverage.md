---
id: computing-software.qa-testing-engineering.test-case-design.functional-completeness-coverage
name: functional-completeness-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [functional-completeness, functional-suitability, requirements-coverage, iso-25010, gap-analysis]
level: practitioner
status: gated
description: "Assess functional completeness: map specified tasks and requirements to implemented functions and tests to find missing functions and untested features."
sources:
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functional completeness

**Goal:** the set of functions covers all specified tasks and user objectives (ISO 25010 functional completeness) (gated: unconfirmed, source is paywalled or blocked).

## Procedure
1. List specified tasks/requirements (backlog, spec, contract, regulatory list).
2. Map each to the implemented function (screen, API endpoint, job) and to tests (`requirements-traceability-matrix`).
3. Classify gaps:
   - specified but not implemented (missing function),
   - implemented partly (only some roles, some data types, some channels like web but not mobile),
   - implemented but not specified (gold plating or undocumented behaviour, which also needs tests),
   - implemented but untested.
4. Also compare against an **external checklist**: regulatory requirements, accessibility, data subject rights (export/delete), audit logging, admin functions people forget (user deactivation, password reset by admin).

## Output
A coverage table: requirement, implemented (Y/partial/N), tested (Y/N), notes. Summarise completeness % and list partials explicitly.

## Gotchas
- "Implemented" in the tracker does not mean deployed and enabled (feature flag off). Check the actual environment.
- API-only implementations of a UI requirement count as partial.

## Verify
Each requirement has an implemented status verified on the test environment and at least one executed test.

## Checked

2026-10-28. Confirmed: Nothing; the ISO 25000 page could not be fetched. Gated: ISO 25010 functional completeness definition. Removed: Syllabus section number and the erroring ISTQB source link.

Method: documentation only; no commands were run.
