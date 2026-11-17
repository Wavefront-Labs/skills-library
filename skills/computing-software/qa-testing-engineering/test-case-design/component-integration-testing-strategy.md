---
id: computing-software.qa-testing-engineering.test-case-design.component-integration-testing-strategy
name: component-integration-testing-strategy
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [component-integration-testing, incremental-integration, test-levels, top-down-integration, bottom-up-integration, big-bang-integration, stubs-and-drivers, test-stubs-drivers]
level: practitioner
status: docs-checked
description: "Plan component integration testing: choose big-bang, top-down, bottom-up or risk-driven incremental order, with the stubs and drivers each order needs."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://martinfowler.com/bliki/IntegrationTest.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Component integration testing strategy

**Goal:** find interface and interaction defects between components in an order that keeps failures easy to localise.

## What to test at integration
Interfaces and data passing (types, units, null/empty), protocol and sequence of calls, error propagation, transactions across components, shared resources (DB, queues), configuration wiring.

## Orders
| Strategy | How | Needs | Use when |
|---|---|---|---|
| Big-bang | All at once | Nothing | Tiny systems only; failures hard to localise |
| Top-down | From UI/controller down | Stubs for lower layers | Early end-to-end skeleton matters |
| Bottom-up | From data/core up | Drivers (test harness) | Core logic is high risk |
| Sandwich / risk-driven | High-risk interfaces first | Both | Most real projects |
| Continuous | Every merge in CI | Contract tests + service tests | Microservices, CD |

## Practice
- Narrow integration tests: one service + real DB + stubs for other services.
- Broad integration tests: several real services; keep few, they are slow and flaky.
- Microservices: replace most broad tests with consumer-driven contract tests (`pact-consumer-tests`).

## Gotchas
- Integration tests that duplicate unit tests through a slower path waste time. Assert on the *interaction*, not the business logic.
- Stubs drift from reality; verify them with contract tests.

## Verify
For each interface in the architecture diagram, there is at least one test exercising it with real serialisation.

## Checked

2026-10-28 Confirmed against: Martin Fowler IntegrationTest (narrow versus broad integration tests); Practical Test Pyramid (consumer-driven contract tests, Pact). Removed or generalised: the ISTQB section number and the Testcontainers name (not in the fetched pages). The orders table (big-bang, top-down, bottom-up, risk-driven) is general practice with no figures.

Method: documentation only; no commands were run.
