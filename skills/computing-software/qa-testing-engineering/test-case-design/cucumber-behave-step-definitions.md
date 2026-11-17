---
id: computing-software.qa-testing-engineering.test-case-design.cucumber-behave-step-definitions
name: cucumber-behave-step-definitions
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [cucumber, step-definitions, behave, bdd, cucumber-expressions, glue-code, world-context, pytest-bdd]
level: practitioner
status: verified
description: "Implement Gherkin steps in Cucumber (JS/Java) and behave/pytest-bdd (Python): expressions, shared context, hooks, reusable steps and keeping glue code thin."
sources:
  - https://cucumber.io/docs/cucumber/step-definitions/
  - https://behave.readthedocs.io/en/stable/
  - https://pytest-bdd.readthedocs.io/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step definitions (Cucumber, behave, pytest-bdd)

**Goal:** thin glue code that maps steps to a domain/driver layer, so scenarios stay readable and steps stay reusable.

## Cucumber-JS
```js
const { Given, When, Then, Before } = require('@cucumber/cucumber')
Given('{word} is a gold customer', async function (name) {
  this.customer = await this.api.createCustomer({ name, tier: 'gold' })   // World holds state
})
When('she buys {int} {string}', async function (qty, sku) {
  this.order = await this.api.order(this.customer.id, sku, qty)
})
Then('she is charged {float}', function (amount) {
  expect(this.order.total).toBe(amount)
})
Before({ tags: '@db' }, async function () { await resetDb() })
```
Run: `npx cucumber-js --tags "@smoke and not @wip"` (run with @cucumber/cucumber; the snippet needs an assertion import such as `const { expect } = require('chai')`, since `expect` is not global in Cucumber-JS).

## behave (Python)
```python
from behave import given, when, then
@given('{name} is a gold customer')
def step_gold(context, name):
    context.customer = context.api.create_customer(name=name, tier="gold")
```
Hooks in `features/environment.py` (`before_scenario`, `after_scenario`). Run `behave --tags=@smoke` (run with behave 1.3.3; the `{name}` step and `before_scenario`/`after_scenario` hooks worked).
pytest-bdd uses `scenarios("features/discount.feature")` plus `@given(parsers.parse(...))` and pytest fixtures for state.

## Rules
- Steps call a domain layer (API client, page objects), never contain raw selectors or SQL.
- Prefer Cucumber Expressions (`{int}`, `{string}`, custom parameter types) over regex.
- State lives in World/context per scenario; never module globals (parallel runs break).
- Avoid near-duplicate step phrasings; maintain a step catalogue (`npx cucumber-js --dry-run --format usage`).

## Gotchas
- Ambiguous step definitions (two matching patterns) fail at run time; `--dry-run` catches them (run: a second `{word}` pattern made one scenario report as ambiguous, the others skipped). The pytest-bdd form (`scenarios(...)` plus `@given(parsers.parse(...))`) passed.
- Undefined steps print a snippet; do not paste snippets blindly into a giant steps file. Organise by domain.

## Verify
`--dry-run` shows no undefined or ambiguous steps, and the usage report shows no unused steps.
