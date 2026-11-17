---
id: computing-software.qa-testing-engineering.cypress.overwriting-commands-and-queries
name: overwriting-commands-and-queries
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [overwrite-command, cypress-overwrite, add-query, custom-commands]
level: practitioner
status: verified
description: "Overwrite built-in Cypress commands (visit, type) with Cypress.Commands.overwrite, write retryable custom queries with addQuery, and avoid breaking retry-ability."
sources:
  - https://docs.cypress.io/api/cypress-api/custom-commands#Overwrite-Existing-Commands
  - https://docs.cypress.io/api/cypress-api/custom-queries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overwriting commands and queries

## Overwrite a command
```js
// mask passwords in the command log
Cypress.Commands.overwrite('type', (originalFn, element, text, options) => {
  if (options && options.sensitive) {
    options.log = false;
    Cypress.log({ $el: element, name: 'type', message: '*'.repeat(text.length) });
  }
  return originalFn(element, text, options);
});
cy.get('#password').type(secret, { sensitive: true });

// default baseUrl-relative visit with auth header
Cypress.Commands.overwrite('visit', (originalFn, url, options = {}) =>
  originalFn(url, { ...options, headers: { 'x-e2e': '1', ...options.headers } }));
```
Always `return originalFn(...)` so the chain yields correctly.

## Custom query (retryable)
A command added with `Commands.add` is not itself a query. For a reusable selector helper that is guaranteed to retry with assertions, use `addQuery` (v12+); a plain `Commands.add('getByCy', id => cy.get(...))` wrapper also retried in a 16.2.0 run (element appearing 2 s late, and a child added late under an existing parent), so the wrapper is not broken, `addQuery` is just the documented contract:
```js
Cypress.Commands.addQuery('getByCy', function (id, options = {}) {
  const getFn = cy.now('get', `[data-cy="${id}"]`, options);
  return (subject) => getFn(subject);   // called repeatedly until assertions pass
});
cy.getByCy('total').should('contain', '$42');
```
Rules: the outer function runs once (set up), the returned inner function must be synchronous and side-effect free; no `cy.*` commands inside it.

## Overwrite a query
`Cypress.Commands.overwriteQuery('get', function (originalFn, ...args) { return originalFn.apply(this, args) })` (ran: the wrapper was called once for one `cy.get`).
Built-in queries must use `overwriteQuery`: since 16.0.0 this includes `getCookie`, `getCookies`, `getAllCookies`, `getAllLocalStorage` and `getAllSessionStorage`, and `Commands.overwrite('getCookie', ...)` throws "Queries can only be overwritten with `Cypress.Commands.overwriteQuery()`".

## Gotchas
- Wrapping `cy.get` in `Commands.add('getByCy', id => cy.get(...))` retried correctly even with a chained `.find()` in 16.2.0; prefer `addQuery` anyway for the explicit retry contract and so overwrites use `overwriteQuery`.
- Overwrites are global: put them in `support/e2e.js`, document them.
- TypeScript: declare signatures in `cypress/support/index.d.ts`.

## Verify
Run on Cypress 16.2.0: `overwrite('type', ...)` with `sensitive`, `overwrite('visit', ...)` (the server saw `x-e2e: 1`), `overwriteQuery('get', ...)`, `addQuery('getByCy', ...)`. `cy.getByCy('late-element').should('be.visible')` passes when the element appears after 2s.
