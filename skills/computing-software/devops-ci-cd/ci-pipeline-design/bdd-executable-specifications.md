---
id: computing-software.devops-ci-cd.ci-pipeline-design.bdd-executable-specifications
name: bdd-executable-specifications
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, bdd, gherkin, acceptance-tests]
level: practitioner
status: gated
description: "Write acceptance criteria as executable Gherkin specifications (Cucumber, Behave, SpecFlow/Reqnroll) that run in the pipeline without becoming a brittle second codebase."
sources: ["https://cucumber.io/docs/gherkin/reference/", "https://www.oreilly.com/library/view/continuous-delivery-reliable/9780321670250/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BDD and executable specifications

Acceptance tests should express business behaviour and be executable (Continuous Delivery, acceptance testing chapter) (gated: unconfirmed, source is paywalled or blocked). Gherkin gives a shared language; step definitions bind it to an application driver layer.
Gherkin gives a shared language; step definitions bind it to an application driver layer.

```gherkin
Feature: Checkout discounts
  Rule: Loyalty members get 10% off orders over 50
    Scenario: Member order above threshold
      Given a loyalty member "ana"
      And a cart worth 80.00
      When she checks out
      Then she pays 72.00
```
```python
# behave steps (Python)
@given('a cart worth {amount:f}')
def step_cart(ctx, amount): ctx.cart = ctx.driver.cart_with_total(amount)
@when('she checks out')
def step_checkout(ctx): ctx.receipt = ctx.driver.checkout(ctx.user, ctx.cart)
@then('she pays {amount:f}')
def step_pay(ctx, amount): assert ctx.receipt.total == amount
```
Steps call a **driver layer** (API client/page objects), never raw selectors, so UI changes touch one place.

## Pipeline
- Tag scenarios: `@smoke` for post-deploy checks, `@wip` excluded from CI.
- JUnit/Cucumber JSON output for reports, published as test results.
- Run against the deployed candidate in the acceptance stage, in parallel by feature file.

## Avoiding the usual failure
- Write scenarios with product/QA **before** implementation (three amigos); otherwise Gherkin is
  just verbose test code.
- Declarative steps ("she checks out"), not imperative ("click #btn-12").
- Keep scenario count modest; push combinatorics down to unit tests.
- Reuse steps through parameters, not copy-paste.

## Verify
- [ ] Scenarios run in CI with readable reports; a product owner can read the feature files.

## Checked

2026-10-28. Confirmed in the Cucumber Gherkin reference: the Rule keyword and Given/When/Then roles. The Continuous Delivery book attribution could not be confirmed (publisher page blocked): gated: unconfirmed, source is paywalled or blocked. Removed: behave command-line options.

Method: documentation only; no commands were run.
