---
id: computing-software.qa-testing-engineering.test-automation.fluent-page-objects
name: fluent-page-objects
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [fluent-page-objects, page-object-model, method-chaining, selenium, playwright, test-design-patterns]
level: practitioner
status: docs-checked
description: "Write page object methods that return the page the user lands on (or this, for fluent chaining), with separate methods per outcome and assertions kept in tests."
sources:
  - https://www.selenium.dev/documentation/test_practices/
  - https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
  - https://martinfowler.com/bliki/PageObject.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluent page objects and navigation returns

**Goal:** page object methods return the page object the user lands on, so tests read as a journey and the type system shows where navigation goes.

## Rules from the Selenium page object docs
- Methods return other Page Objects, Page Component Objects, or optionally themselves (for fluent syntax).
- An action that does not navigate (typing a username) returns the current page object (`return this`).
- An action that navigates returns a new page object for the destination. The docs' `submitLogin()` returns `HomePage`; if the login page later went somewhere else (their example: a legal disclaimer), changing the method signature makes every dependent test fail to compile.
- Different results for the same action are different methods: `submitLogin()` (expects success, returns `HomePage`) and `submitLoginExpectingFailure()` (returns `LoginPage`). If the wrong page appears, instantiating the expected page object fails the script.
- A higher-level service method such as `loginAs(user, password)` reuses the granular methods rather than repeating them.
- The constructor may verify that the driver is on the right page (the docs check the title and throw `IllegalStateException`); this is the accepted exception to "no assertions in page objects".
- Page objects generally do not assert; the test does (`assertThat(homePage.getMessageText(), is("Hello userName"))`).

## Fowler's view
Page object operations should return fundamental types (strings, dates) or other page objects. Fowler notes some practitioners prefer page objects to return a generic browser context and let the test choose the next page object, since the test knows the flow (especially conditional flows) and statically typed languages reveal navigation in signatures. Treat navigation-returning as a common choice, not a rule. He favours no assertions in page objects, with invariant checks as acceptable.

## Illustrative Playwright variant (not from the pages)
```ts
async loginAs(email: string, pw: string): Promise<DashboardPage> {
  await this.page.getByLabel('Email').fill(email);
  await this.page.getByLabel('Password').fill(pw);
  await this.page.getByRole('button', { name: 'Sign in' }).click();
  return new DashboardPage(this.page);
}
```

## Verify
Tests read as chains of user intents, a navigation to the wrong page fails at the transition, and page objects hold no assertions beyond loaded checks.

## Checked
2026-11-08. Confirmed against the Selenium page object models page (summary list, `LoginPage` example, `return this`, separate failure method, constructor check) and Fowler's PageObject bliki (return types, alternative generic-context preference, assertion debate). Removed: the Java `d.findElement` example with `data-testid` locators, the claim that async chains are awkward in Playwright and that one method per step is preferred (not in the pages), and the Selenium test_practices landing page, which has no detail on this topic. The Playwright snippet is kept only as a labelled illustration.
Method: documentation only; no commands were run.
