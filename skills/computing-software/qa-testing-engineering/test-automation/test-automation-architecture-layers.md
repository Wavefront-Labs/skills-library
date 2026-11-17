---
id: computing-software.qa-testing-engineering.test-automation.test-automation-architecture-layers
name: test-automation-architecture-layers
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-automation-architecture, test-automation-strategy, generic-taa, test-adaptation-layer, framework-design, istqb-tae]
level: practitioner
status: draft
description: "Structure a test automation framework in layers: test definition, execution, adaptation (drivers/clients), plus configuration, data, logging and reporting."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test automation architecture (TAA)

**Goal:** a framework where tests survive UI/API changes and tools can be swapped. ISTQB CTAL-TAE generic TAA.

## Layers
1. **Test generation** (optional): models or data generating tests.
2. **Test definition**: the tests themselves, readable, in business terms: `checkout.pay_with_saved_card(order)`.
3. **Test execution**: runner (pytest/JUnit/Playwright Test), fixtures, parallelism, retries, reporting.
4. **Test adaptation**: everything that talks to the SUT: page objects/components, API clients, DB helpers, message clients, device drivers. Tool-specific code lives only here.

Cross-cutting: configuration (env URLs, credentials via env vars/secrets), test data management, logging (step logs, screenshots, HAR), reporting.

## Example layout
```
tests/            # definition: specs grouped by feature
  checkout/test_pay.py
framework/
  api/            # adaptation: typed API clients
  pages/          # adaptation: page objects/components
  data/           # builders, factories
  config.py       # env selection
conftest.py       # execution: fixtures wiring layers together
```

## Rules
- Tests never import the driver (Selenium/Playwright) directly.
- No assertions inside the adaptation layer (except waits); tests decide pass/fail.
- One place per concept: one login helper, one way to create a user.

## Gotchas
- Over-engineering: five abstraction layers for 30 tests. Grow the architecture with the suite.
- Framework owned by one person becomes a bottleneck; document and review it like product code.

## Verify
Changing a selector or endpoint requires editing one file in the adaptation layer, not tests.
