---
id: computing-software.qa-testing-engineering.test-automation.test-code-standards-and-review
name: test-code-standards-and-review
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-code-standards, test-code-review, clean-tests, test-automation, code-review]
level: practitioner
status: draft
description: "Define test code standards and review guidelines: naming, structure (arrange-act-assert), independence, no sleeps, assertions, locators, data handling and a PR checklist."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test code standards and review guidelines

**Goal:** test code held to production code standards so the suite stays readable, reliable and cheap to maintain.

## Standards
- **Naming:** test names describe behaviour and condition: `rejects_order_when_card_expired`, `should show error when email is taken`. One behaviour per test.
- **Structure:** arrange-act-assert (or given-when-then) with blank lines between; setup in fixtures/builders, not copy-paste.
- **Independence:** no test depends on another's side effects or order; each creates its own data; runs in parallel and in random order.
- **Synchronisation:** no fixed sleeps; use framework auto-waits, explicit conditions or polling assertions.
- **Assertions:** assert outcomes the user or caller cares about; specific messages; no assertion-free tests; avoid asserting implementation details or entire snapshots when one field matters.
- **Locators:** user-facing roles/labels or `data-testid`; no brittle XPath on layout.
- **Data:** builders/factories with defaults, unique values; no hard-coded production-like personal data or secrets.
- **Abstractions:** page objects/app actions hold the how; tests read as the what. Avoid deep inheritance hierarchies.
- **Lint and format** test code with the same tools; enable framework lint plugins (`eslint-plugin-playwright`, `eslint-plugin-jest`, `flake8-pytest-style`).

## PR review checklist for tests
- Does the test fail if the feature breaks? (Mutate the code or assertion to check.)
- Is it at the lowest sensible layer?
- Any sleeps, random data without seeds, shared state, order dependence?
- Clear name and failure message?
- Is it tagged correctly (smoke, slow, requirement ID)?
- Did it run green several times (`--repeat-each=5`, `pytest --count`)?

## Verify
Standards are in the repo (CONTRIBUTING or docs), lint rules enforce the mechanical parts, and test PRs are reviewed with the checklist.
