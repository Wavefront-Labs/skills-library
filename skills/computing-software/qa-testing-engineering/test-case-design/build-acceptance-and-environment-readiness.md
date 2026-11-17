---
id: computing-software.qa-testing-engineering.test-case-design.build-acceptance-and-environment-readiness
name: build-acceptance-and-environment-readiness
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [build-acceptance-test, environment-readiness, entry-criteria, smoke-test, test-environment]
level: practitioner
status: draft
description: "Gate test execution with entry checks: build acceptance (smoke) tests, environment readiness checklist, test data and integration availability before testing starts."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build acceptance test and environment readiness

**Goal:** testers only start on a build and environment that can be tested, so time is not wasted on broken deployments (entry criteria, ISTQB CTFL 5.1.3).

## Environment readiness checklist
- Correct build version deployed on every component (version endpoint or build info page matches the release candidate).
- Configuration matches the target (feature flags, endpoints, certificates).
- Dependencies reachable: databases, queues, third-party sandboxes, SSO; health endpoints green.
- Test data loaded and masked; test accounts per role work.
- Monitoring/logging accessible to testers.
- Test tools ready: automation agents, device farm access, licences.

Automate the checklist as a script that prints pass/fail per item; run it after every deploy.

## Build acceptance test (BAT / smoke)
- 10-30 minutes maximum, automated, covering: app starts, login per role, one happy path per critical journey, a key integration call, no errors in logs at startup.
- Runs automatically after deployment to the test environment; a red BAT rejects the build back to development with the failing check.
- The BAT is not regression: keep it short and stable.

## Process
1. Deploy, run readiness script and BAT.
2. Both green: announce "build N accepted for testing".
3. Any red: record a build rejection (count them: a metric of delivery quality), notify dev, keep testing the previous accepted build.

## Verify
Every build entering test has a recorded readiness and BAT result, and rejected builds have a logged reason.
