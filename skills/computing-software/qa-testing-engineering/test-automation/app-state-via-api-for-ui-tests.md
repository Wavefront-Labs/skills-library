---
id: computing-software.qa-testing-engineering.test-automation.app-state-via-api-for-ui-tests
name: app-state-via-api-for-ui-tests
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [app-state-via-api, test-setup, ui-test-speed, test-isolation, api-seeding]
level: practitioner
status: docs-checked
description: "Prepare UI test state through APIs instead of the browser: log in by API and set a cookie, seed data via existing APIs, with Playwright request contexts and Cypress cy.session."
sources:
  - https://www.selenium.dev/documentation/test_practices/encouraged/generating_application_state/
  - https://playwright.dev/docs/api-testing
  - https://docs.cypress.io/app/core-concepts/best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating application state via API instead of UI

**Goal:** UI tests spend their time on the behaviour under test; repetitive preparation happens through other means.

## Selenium guidance
The Selenium page says Selenium should not be used to prepare a test case. Repetitive actions and preparation should use other methods. For example, most UIs have a login form; skipping the browser login before every test improves speed and stability. Create a method to gain access to the application under test (the page's example: use an API to log in and set a cookie). Do not pre-load test data through Selenium either; use existing APIs to create it.

## Playwright
- `APIRequestContext` can send requests without loading a page. The docs list uses: testing the server API, preparing server-side state before visiting the web app in a test, and validating server-side post-conditions after browser actions.
- The `request` fixture respects `baseURL` and `extraHTTPHeaders` from config. Create a context manually with `playwright.request.newContext()` in `beforeAll` (and `dispose()` it in `afterAll`) to reuse it across tests in a file.
- The docs' precondition example creates an issue through the API, then opens the page and checks it appears first.
- Reusing authentication: authenticated state is held as cookies; `apiRequestContext.storageState()` can export it and a new browser context can be created with that state, so you log in by API and start the browser already authenticated. Storage state is interchangeable between `BrowserContext` and `APIRequestContext`.
- A context request from `browserContext.request` or `page.request` shares cookies with the browser context and updates them from `Set-Cookie`; a context from `apiRequest.newContext()` has isolated cookies.

## Cypress
The best-practices page lists as an anti-pattern using the UI to log in and not taking shortcuts; the best practice is to test specs in isolation, log in programmatically and take control of application state (it points to its Logging in recipes). `cy.request()` can talk to servers via their APIs, and `cy.session()` caches results to avoid repeated logins or visits.

## Verify
Tests begin on the page under test with state ready. Suite time drops and the login flow itself is still covered by its own test (that last point is practitioner judgement, not stated in the sources).

## Checked
2026-11-08. Confirmed against the Selenium generating-state page, Playwright API testing page and Cypress best-practices page. Removed (not in the sources): the Playwright `context.addCookies` snippet, the "setup project" for storageState, the Cypress seed-endpoint snippet, the Java `addCookie` snippet, test-only `/api/test/*` endpoint advice, DB factories, and the gotchas about API versus UI state differences and SameSite cookies. Added the cookie-sharing behaviour of the Playwright context types.
Method: documentation only; no commands were run.
