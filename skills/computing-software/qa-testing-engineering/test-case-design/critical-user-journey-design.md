---
id: computing-software.qa-testing-engineering.test-case-design.critical-user-journey-design
name: critical-user-journey-design
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [user-journeys, critical-user-journeys, scenario-based-testing, end-to-end-testing, e2e-test-selection, analytics-driven-testing]
level: practitioner
status: docs-checked
description: "Identify and design end-to-end tests for critical user journeys using analytics, revenue impact and support tickets, keeping the E2E layer small."
sources:
  - https://sre.google/workbook/implementing-slos/
  - https://martinfowler.com/articles/practical-test-pyramid.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Critical user journey design

**Goal:** a small set of end-to-end tests that cover the journeys whose failure hurts most. Google SRE Workbook (CUJs); Practical Test Pyramid.

## Identify journeys
1. List journeys from product analytics (top funnels by traffic), revenue (checkout, subscription), legal/compliance (consent, data export), support tickets (what users complain about).
2. Score: business impact x usage x change frequency.
3. Pick the top few as critical, keeping the list short; write them as a sentence: "A returning customer finds a product by search, adds it, pays with saved card, and gets a confirmation email".

## Design each E2E test
- One journey per test; data set up via API, UI only for the journey itself.
- Assert business outcomes at each milestone (order created with right total), not every pixel.
- Include one key failure variant only where it is critical (payment declined path).
- Run against production-like envs on every deploy; a subset as synthetic monitoring in production.

## Keep the layer small
Edge cases go to lower levels (API, component, unit). E2E answers "is the wiring working", not "is every rule right".

## Gotchas
- Long journeys that do everything become flaky and slow to debug; split at natural checkpoints.
- Journeys go stale when the product changes; review the list regularly with product.

## Verify
Every journey on the critical list has an automated E2E test in the deploy pipeline and an owner.

## Checked

2026-10-28 Confirmed against: Google SRE Workbook, Implementing SLOs (critical user journeys); Practical Test Pyramid (end-to-end and UI tests as the top layer). Removed or generalised: the 5-15 journey count and the quarterly review cadence (not sourced).

Method: documentation only; no commands were run.
