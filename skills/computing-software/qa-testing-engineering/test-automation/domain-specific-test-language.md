---
id: computing-software.qa-testing-engineering.test-automation.domain-specific-test-language
name: domain-specific-test-language
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [test-dsl, domain-specific-language, test-automation-patterns, readable-tests, fluent-api]
level: practitioner
status: docs-checked
description: "Build a domain-specific language layer for tests: business-vocabulary methods over drivers, hiding UI mechanics, and keeping the DSL thin and reviewed."
sources:
  - https://www.selenium.dev/documentation/test_practices/encouraged/domain_specific_language/
  - https://martinfowler.com/bliki/BusinessReadableDSL.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain-specific language layer for tests

**Goal:** tests written in the language of the business ("create a new account", "order displayed results by name"), with a layer below that translates to UI or API calls. Selenium lists this under encouraged practices.

## What Selenium says
- The goal is ubiquitous language: say "create a new account", not "load data into this table" or "click on the third column".
- With Selenium a DSL is usually a set of methods written to keep the API simple and readable, giving developers and stakeholders a shared vocabulary.
- Benefits listed: readable (stakeholders can understand it), writable (avoids duplication), extensible (add functionality without breaking contracts), maintainable (implementation detail stays out of test cases, so UI changes touch the DSL method, not every test).
- Test scripts should read like a list of things the user wants to DO and to KNOW, and should not concern themselves with how the UI requires it.

## Layering
1. **Test cases**: only DSL calls and expectations.
2. **DSL methods**: domain verbs and nouns, e.g. `login_as_user(username, password)` that clears and fills the fields, clicks submit and returns the next page object.
3. **Drivers**: page/component objects, API clients.

```python
def test_gold_customer_gets_free_shipping(shop):
    shop.register_customer("alice", tier="gold")
    shop.add_to_basket("alice", "coffee-beans", qty=2)
    shop.checkout("alice")
    shop.assert_shipping_cost("alice", 0)
```

## Design rules
- Verbs come from the domain language (story text, stakeholder vocabulary), not UI terms (`click`, `fill`).
- Default every optional input; tests state only what matters.
- Keep branching logic out of tests; put it in the DSL.

## Business-readable, not business-writable
Martin Fowler: the sweet spot is a DSL business people can read rather than write. Programmers write the code and show it often to business people who confirm what it means. A business-writable DSL raises cost because it needs a decent editing environment, meaningful error messages, and debugging and testing tools.

## Gotchas
- The DSL becomes a second application; keep it thin and review it like production code.
- Over-generic methods (`do_action(name, params)`) lose readability; prefer explicit verbs.

## Verify
A product owner can read a test and say whether it matches the requirement.

## Checked
2026-11-09: checked against the two cited pages, read in full: Selenium "Domain specific language" (ubiquitous language, benefits, the `loginAsUser` example, UI-is-secondary guidance) and Fowler "Business Readable DSL" (readable versus writable, cost of a writable DSL). Removed: the attribution of a four-layer acceptance model to Dave Farley (not in either page), UUID alias isolation and parallel-run claims, and the CI driver-swap check, none of which the pages state. The code sample is illustrative, not from the pages.

Method: documentation only; no commands were run.
