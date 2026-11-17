---
id: computing-software.qa-testing-engineering.cypress.conditional-testing-safely
name: conditional-testing-safely
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [conditional-testing, cypress-core-concepts, deterministic-tests, flaky-tests, test-state-control]
level: practitioner
status: verified
description: "Avoid flaky conditional logic in Cypress: why 'if element exists' is unreliable, control state instead, and the safe patterns when a branch is unavoidable."
sources:
  - https://docs.cypress.io/app/guides/conditional-testing
  - https://docs.cypress.io/app/core-concepts/retry-ability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional testing safely (Cypress)

**Goal:** deterministic tests. "If the cookie banner is visible, close it" is the classic source of flakes: the DOM may not have settled when you check.

## Why it fails
The app is asynchronous; at the moment you query, the element may not exist yet but appear 50 ms later. Cypress retries assertions, but a conditional check has no assertion to retry, so you read a moment in time.

## Prefer controlling state
- Cookie banner: set the consent cookie/localStorage before visit (`cy.setCookie('consent', 'yes')`).
- A/B tests: force the variant via query param, cookie, or stub the flag API with `cy.intercept`.
- Onboarding/tour modals: seed the user as "onboarded" via API.
- Server data: seed exactly what the test needs instead of branching on what is there.

## When a branch is unavoidable
Make the condition depend on something already stable:
```js
// 1. Wait for a known stable element first, then inspect synchronously
cy.get('[data-cy=app-ready]').should('exist');
cy.get('body').then(($body) => {
  if ($body.find('[data-cy=promo-modal]').length) {
    cy.get('[data-cy=promo-modal] [data-cy=close]').click();
  }
});

// 2. Branch on server response, not DOM
cy.intercept('GET', '/api/flags').as('flags');
cy.visit('/');
cy.wait('@flags').its('response.body.newCheckout').then((on) => {
  if (on) { cy.get('[data-cy=new-checkout]').click(); } else { cy.get('[data-cy=checkout]').click(); }
});
```
Also: `cy.url().then(url => ...)` after a navigation assertion has passed.

## Anti-patterns
- `cy.get(sel).then(...)` to check existence (fails the test if absent, never takes the else branch).
- `cy.wait(1000)` before a conditional.
- try/catch around commands (does not work; failures are not exceptions in your code).

## Verify
Run on Cypress 16.2.0: the `cy.get('body').then(...find...)` and `cy.wait('@flags').its(...)` branches work; try/catch around `cy.get` never reaches the catch (the test just fails), and `cy.get(sel).then(...)` on a missing element fails the test instead of taking an else branch. No conditional depends on DOM state that is still loading, and tests that set state explicitly pass 50 repeated runs.
