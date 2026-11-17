---
id: computing-software.qa-testing-engineering.test-automation.app-actions-vs-page-objects
name: app-actions-vs-page-objects
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [app-actions, page-object-model, cypress, test-setup, test-design-patterns]
level: practitioner
status: docs-checked
description: "Use app actions (calling application code or APIs directly for setup) versus page objects: when each fits, Cypress window access, API seeding, UI sync."
sources:
  - https://www.cypress.io/blog/stop-using-page-objects-and-start-using-app-actions
  - https://playwright.dev/docs/api-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App actions vs page objects

**Goal:** reach the state a test needs quickly and reliably, using the UI only for the behaviour under test.

## The idea
Page objects drive the UI for everything, including setup. **App actions** bypass the UI to set state: calling the application's own functions, exposed for tests, so a test sets state directly and then checks only the screen of interest (Gleb Bahmutov, Cypress blog). In that article, entering three todo items through the UI before each test took most of a context's 4-5 second run time; app actions removed that cost. The article is an opinion piece; page objects remain widely and successfully used in the Cypress ecosystem.

## Cypress example (exposed model)
The blog attaches the app's model object to `window` only when running under Cypress, then calls its existing `addTodo` method:

```js
// app code
var model = new app.TodoModel('react-todos');
if (window.Cypress) {
  window.model = model
}
// test
cy.window().its('model').invoke('addTodo', 'write tests');   // app action for setup
// then assert in the UI on what matters
```

## API-based variant (any framework)
Playwright's `request` fixture sends API requests (`request.post(url, { data: ... })`), so setup can use the app's HTTP API:

```ts
test('shows order in history', async ({ page, request }) => {
  const order = await (await request.post('/api/orders', { data: { sku: 'ABC' } })).json();
  await page.goto('/orders');
  await expect(page.getByText(order.id)).toBeVisible();
});
```
The `/api/orders` endpoint is a placeholder for your own API.

## Synchronise with the UI
App actions can run ahead of the application, so a test can look flaky because of a race between test and app. The blog's recommended pattern: run an app action, assert that the UI reached the expected state, then run the next app action. A user could not toggle an item before it is shown, so wait for it to appear first.

## When to use which
- **App actions/API:** login, seeding data, reaching deep states, preconditions repeated across tests. Faster and less flaky.
- **Page objects:** the flows themselves under test, especially critical journeys that must be exercised through the real UI at least once.
- Mix both: each UI flow is tested through the UI once; other tests use app actions to get there.

## Cautions
- Exposing internals (`window.model`) must be limited to test runs (the `window.Cypress` guard) and never ship to production.
- App actions couple tests to internal APIs; prefer public HTTP APIs where possible.
- Keep a coverage check: every UI flow bypassed by app actions still has at least one UI-driven test.

## Verify
Setup steps in UI tests use app actions or API calls, suite runtime drops measurably, and each bypassed UI flow still has a dedicated UI-driven test.

## Checked
2026-11-09. Confirmed in the Cypress blog post (window.Cypress guard, window.model, cy.window().its().invoke('addTodo'), 4-5 second figure, race and wait-then-act pattern, opinion note) and the Playwright API testing page (`request` fixture, `request.post` with `data`). Fixed: the example exposed `window.app`; the article uses `window.model`. Removed: the docs.cypress.io and playwright intro sources (landing pages), the `data-testid=todo-item` assertion.
Method: documentation only; no commands were run.
