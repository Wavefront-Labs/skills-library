---
id: computing-software.qa-testing-engineering.cypress.cross-origin-with-cy-origin
name: cross-origin-with-cy-origin
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-origin, cross-origin-testing, cypress-network, multi-domain, cypress-sso]
level: practitioner
status: verified
description: "Test flows across domains with cy.origin: run commands on another superdomain, pass arguments, share dependencies, and combine with cy.session for SSO login."
sources:
  - https://docs.cypress.io/api/commands/origin
  - https://docs.cypress.io/app/guides/cross-origin-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-origin flows with cy.origin

**Goal:** test flows that leave your app's origin (identity provider, payment page, partner site) and come back. GA since Cypress 12.

## Basic usage
```js
cy.visit('/checkout');
cy.get('[data-cy=pay-with-provider]').click();       // navigates to https://pay.provider.test
cy.origin('https://pay.provider.test', () => {
  cy.get('input[name=card]').type('4242424242424242');
  cy.contains('button', 'Pay').click();
});
cy.url().should('include', '/checkout/complete');     // back on the app origin
```

## Passing data
The callback is serialised and run in the other origin; closures do not work. Pass values with `args`:
```js
cy.env(['PW']).then(({ PW }) => {            // Cypress 16: Cypress.env() was removed; cy.env() keeps secrets in Node
  const user = { email: 'alice@example.test', password: PW };
  cy.origin('https://login.idp.test', { args: user }, ({ email, password }) => {
    cy.get('#email').type(email);
    cy.get('#password').type(password, { log: false });
    cy.get('button[type=submit]').click();
  });
});
```
Load modules inside: `Cypress.require('../support/helpers')` (added in 12.6.0; the path is relative to the spec, and on 16.2.0 it needs `e2e: { experimentalOriginDependencies: true }`, otherwise it throws). A closure variable inside the callback gives `ReferenceError: x is not defined`, and a custom command registered in the spec was `cy.mycmd is not a function` inside the callback, so re-register commands or import them there.

## With cy.session (SSO login once)
```js
Cypress.Commands.add('loginViaIdp', (user) => {
  cy.session(user.email, () => {
    cy.visit('/login');
    cy.origin('https://login.idp.test', { args: user }, ({ email, password }) => { /* fill form */ });
    cy.url().should('include', '/dashboard');
  }, { cacheAcrossSpecs: true });
});
```

## Rules and limits
- Needed whenever the test visits a different origin (scheme, hostname or port), even within one superdomain, since Cypress 14.0.0 stopped injecting `document.domain` (the `injectDocumentDomain` config restores the old behaviour for now; see the 14.0 migration guide). Visiting `127.0.0.1:3457` from `localhost:3456` without it failed with "The command was expected to run against origin ... but the application is at origin ...".
- `cy.intercept` is defined outside `cy.origin` (an intercept for the second origin's URL caught a request made inside the callback).
- Prefer programmatic login (API/token) over UI SSO for most tests; keep one UI SSO test.

## Gotchas
- Identity providers may block automation (bot protection, MFA); use a test tenant with those disabled.
- `chromeWebSecurity: false` is not a substitute for `cy.origin`.

## Verify
The cross-origin flow passes (run here in Electron only; other browsers were not tried) and SSO login is cached with cy.session across specs.
