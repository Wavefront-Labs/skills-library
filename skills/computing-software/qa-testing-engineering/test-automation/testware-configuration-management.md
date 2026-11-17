---
id: computing-software.qa-testing-engineering.test-automation.testware-configuration-management
name: testware-configuration-management
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [testware-configuration-management, test-management-tools, version-control, test-environments-as-code, traceability, istqb]
level: practitioner
status: draft
description: "Put testware under configuration management: tests, data, environment definitions and tool configs versioned with the code, and results tied to exact versions."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuration management of testware

**Goal:** any test result can be reproduced: you know exactly which test version ran against which build, data and environment. ISTQB CTFL v4.0 5.4.

## Put under version control
- Automated tests in the **same repo** as the code they test (or a versioned, tagged test repo pinned per release).
- Test data generators, seed scripts, fixtures, anonymisation rules.
- Environment definitions: Docker Compose, Helm values, Terraform for test envs.
- Tool configuration: `playwright.config.ts`, `pytest.ini`, JMeter `.jmx`, k6 scripts, CI pipelines.
- Manual test cases/charters if kept as Markdown, or exported baselines from the test management tool per release.

## Identify what ran
Every test run records: application build/commit SHA, test code commit SHA, environment name and config version, data set version, browser/tool versions. Put these in the report header (JUnit XML properties, Allure environment, CI metadata).

## Baselines
Tag test code at release (`git tag v2.4.0`), so maintenance testing on v2.4.x uses matching tests.

## Gotchas
- Shared test data edited by hand in a test DB is unversioned config; script it.
- Unpinned tool versions (`npx playwright` latest) change results; pin in lockfiles and container tags.

## Verify
Given an old run's report, you can check out the exact test code and environment definition and rerun it.
