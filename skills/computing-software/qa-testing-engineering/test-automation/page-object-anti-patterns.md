---
id: computing-software.qa-testing-engineering.test-automation.page-object-anti-patterns
name: page-object-anti-patterns
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [page-object-anti-patterns, page-object-model, test-design-patterns, test-maintainability, code-smells]
level: practitioner
status: docs-checked
description: "Page object pitfalls the Selenium and Fowler docs warn about: assertions in pages, exposed internals, one page per URL, WebDriver calls in tests and duplicated locators."
sources:
  - https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
  - https://martinfowler.com/bliki/PageObject.html
  - https://playwright.dev/docs/pom
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page object anti-patterns

**Goal:** keep page objects a thin, intention-revealing layer. Each item below is tied to what the sources state.

## Anti-patterns and fixes
- **Assertions inside page objects.** Selenium: page objects should never make verifications; those belong in tests. The one allowed check is that the page (and perhaps critical elements) loaded, done in the constructor. Fowler agrees (no assertions), noting invariant checks are acceptable, and says duplication can be handled with shared assertion libraries instead. Fowler also records the opposing view (assertions reduce duplication and give better messages), so this is a choice, not a universal rule.
- **Exposing page internals.** Selenium summary: public methods are the services the page offers; do not expose the internals of the page or component. Tests that touch locators or WebElements depend on DOM structure.
- **Mirroring the widgets instead of intent.** Fowler: the interface should let a client do and see what a human can, with accessors typed by meaning (strings, booleans, action-named buttons). Selenium models services such as `loginAs(user, password)` on top of granular methods.
- **Test code calling WebDriver directly.** Fowler quotes Simon Stewart: if you have WebDriver APIs in test methods, you are doing it wrong. The Selenium docs show locators intertwined with test logic and spread over many tests as the problem the pattern solves.
- **One page object per page by reflex.** Fowler: build them for significant elements on a page (album list, header, footer); do not expose composite structure that only lays out the UI. Selenium: a page object need not represent an entire page and can be composed of components.
- **Locators defined in several places.** Selenium: only one place in the suite should know the HTML structure of a page or part of one; Playwright: capture selectors in one place.
- **Hiding concurrency badly.** Fowler: page objects can encapsulate asynchrony and threading details so tests do not see them.
- **Putting behaviour in the UI to test through it.** Fowler: a scripting interface is usually better placed underneath the UI; page objects can "make the best of a bad job" when logic has leaked into the UI.

## Verify
Review the page layer: no assertions beyond loaded checks, locators defined once, no WebDriver calls in tests, objects sized to meaningful page parts.

## Checked
2026-11-08. Confirmed against the Selenium page object models page, Fowler's PageObject bliki and the Playwright POM page. Removed (not stated in these pages): god-page size guidance, deep inheritance, sleeps and custom waits, static or global driver and parallel runs, test data in pages, API-based setup, and unused-method cleanup. Replaced the Selenium test_practices landing page source with the dedicated page object page.
Method: documentation only; no commands were run.
