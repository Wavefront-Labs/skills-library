---
id: computing-software.qa-testing-engineering.test-case-design.test-environment-tiers-strategy
name: test-environment-tiers-strategy
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-environment-strategy, environment-tiers, test-levels, test-environments, staging]
level: practitioner
status: docs-checked
description: "Design test environment tiers (dev, CI, SIT, staging, UAT, perf) per test level: purpose, data, fidelity, ownership, promotion and drift control."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://12factor.net/dev-prod-parity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test environment tiers per level

**Goal:** each test level runs where its results mean something, without teams fighting over one shared environment.

## Typical tiers
| Tier | Used for | Data | Fidelity | Owner |
|---|---|---|---|---|
| Local / dev | unit, component, dev checks | fakes, seeds | low | developer |
| CI ephemeral | unit, component integration, contract, API | containers, seeded | medium | pipeline |
| Preview per PR | feature review, exploratory, E2E smoke | synthetic | medium | pipeline |
| SIT / integration | system integration with real third-party sandboxes | synthetic + sandbox accounts | high | QA/platform |
| Staging / pre-prod | system, release regression, OAT, deploy rehearsal | masked production-like | production-like | platform |
| UAT | business acceptance | business-realistic, masked | production-like | business + QA |
| Performance | load/stress/soak | volume-scaled | production-sized | perf team |

## Design rules
- Same artefact promoted through tiers (build once, deploy many); configuration via environment variables.
- Infrastructure as code for every tier so it can be rebuilt; compare tiers with config diffs to catch drift.
- Version manifest per environment (service versions, schema version, feature flags) visible on a dashboard.
- Booking/reservation for shared tiers, or make them ephemeral.
- Production parity where defects hide: same DB engine and version, same OS image, same TLS/proxy setup.

## Gotchas
- Staging with different feature flags or tiny data volumes passes things production fails.
- Third-party sandboxes behave differently from production (rate limits, async callbacks); plan stubs for gaps.
- Shared SIT environments are the main cause of "blocked" tests; track environment downtime as a metric.

## Verify
The test plan names the tier for every test level and type, and each tier's version manifest can be shown on demand.

## Checked

2026-10-28. Confirmed: Twelve-Factor Dev/prod parity: keep dev, staging and production similar; backing services (database engine) are where parity matters; Twelve-Factor Config: configuration via environment. Removed: Nothing removed; tier table is design advice.

Method: documentation only; no commands were run.
