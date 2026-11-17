---
id: computing-software.qa-testing-engineering.test-automation.choosing-the-test-layer
name: choosing-the-test-layer
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-layer-selection, test-pyramid, unit-tests, integration-tests, e2e-testing, test-strategy]
level: practitioner
status: draft
description: "Decide whether a check belongs at unit, integration, contract or end-to-end level: the lowest layer that can catch the defect, with decision questions and examples."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://martinfowler.com/articles/practical-test-pyramid.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing the unit, integration or E2E layer for a test

**Goal:** put each check at the lowest layer that can reliably detect the failure it targets, so suites stay fast and failures point at the cause.

## Decision questions
1. **Is the logic pure and inside one unit** (calculation, validation, mapping, state machine)? Unit test. Cover all partitions and boundaries here.
2. **Does the risk sit in the interaction with a real dependency** (SQL query, ORM mapping, serialisation, message broker config, file system)? Integration test with the real dependency (Testcontainers), not a mock.
3. **Is it an agreement between two services/teams** (request and response shape)? Contract test (Pact or schema-based), not E2E.
4. **Does it need the whole deployed system wired together** (routing, auth across services, config, a critical user journey)? E2E, and only for the journey, not for every rule variant.
5. **Is it about the UI rendering a state** (button disabled when invalid)? Component test (Playwright/Cypress component, Testing Library), not full E2E.

## Examples

| Check | Layer |
|---|---|
| Discount calculation for 12 tier combinations | unit (parameterised) |
| Repository query returns only active customers | integration with real DB |
| Orders service sends the fields billing expects | contract |
| Checkout works end to end with payment sandbox | E2E (one happy path + key failure) |
| Error banner shows on 500 | component test with network stub |

## Push down
When an E2E test fails because of a logic defect, write the lower-level test that would have caught it and keep the E2E as a journey check only.

## Verify
In code review, each new test's layer can be justified with the questions above, and no rule variant is tested only at E2E level.
