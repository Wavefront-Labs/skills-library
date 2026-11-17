---
id: computing-software.qa-testing-engineering.cypress.stubbing-with-fixture-files
name: stubbing-with-fixture-files
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-fixtures, cy-fixture, cy-intercept, fixture-files]
level: practitioner
status: verified
description: "Stub Cypress network responses with fixture files: intercept fixture shorthand, cy.fixture loading, binary encoding, dynamic edits and keeping fixtures in sync with the API."
sources:
  - https://docs.cypress.io/api/commands/fixture
  - https://docs.cypress.io/api/commands/intercept#Stubbing-a-response
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stubbing responses with fixture files

## Files
`cypress/fixtures/` (configurable `fixturesFolder`). JSON, images, CSV, etc.

## Shorthand
```js
cy.intercept('GET', '/api/orders*', { fixture: 'orders/list.json' }).as('orders');
cy.intercept('GET', '/api/avatar/*', { fixture: 'avatar.png,null' });  // binary: encoding null
cy.intercept('POST', '/api/orders', { statusCode: 201, fixture: 'orders/created.json', delay: 300 });
```

## Load and modify
```js
cy.fixture('orders/list.json').then(list => {
  list.items[0].status = 'refunded';
  cy.intercept('GET', '/api/orders*', list);
});
cy.fixture('user.json').as('user');      // reusable via this.user
```
In a 16.2.0 run, mutating the object yielded by one `cy.fixture('orders/list.json')` did not change what a second call yielded (`fx-1` stayed), so per-test edits do not leak; `structuredClone(list)` is still a cheap guard if your Cypress version differs.

## Fixture discipline
- Generate fixtures from real API responses (record once, scrub PII), not hand-written guesses.
- Validate fixtures against the OpenAPI/JSON schema in CI so they don't drift from the backend.
- Keep a few contract-level tests against the real API so stubs alone never define correctness.

## Gotchas
- Path is relative to the fixtures folder (`cypress/fixtures` by default, `fixturesFolder` to change). Passing an encoding yields the raw contents unparsed whatever the extension, and `null` yields a Buffer (docs for `cy.fixture`).
- Large fixtures slow specs; trim to what the UI needs.
- A fixture that does not match the request's expected shape fails silently in the UI; assert something rendered from it.

## Verify
Run on Cypress 16.2.0: JSON fixture stub (`fx-1` rendered in the page), binary shorthand `avatar.png,null` (8 bytes arrived in the page), `cy.fixture(...).as('user')` read via `this.user`. `cy.wait('@orders')` resolves and the UI shows fixture-specific data (e.g. a unique order id).
