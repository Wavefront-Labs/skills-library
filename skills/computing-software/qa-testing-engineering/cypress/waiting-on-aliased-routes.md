---
id: computing-software.qa-testing-engineering.cypress.waiting-on-aliased-routes
name: waiting-on-aliased-routes
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-wait-alias, cy-intercept, cypress-network, network-synchronisation, request-assertions]
level: practitioner
status: verified
description: "Synchronise Cypress tests with network calls using cy.intercept aliases and cy.wait('@alias'): assert request and response, multiple calls, timeouts and ordering."
sources:
  - https://docs.cypress.io/api/commands/wait#Alias
  - https://docs.cypress.io/app/guides/network-requests
  - https://docs.cypress.io/api/commands/intercept
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Waiting on aliased routes (Cypress)

**Goal:** wait for the request the UI depends on, not an arbitrary number of milliseconds.

## Basics
```js
cy.intercept('POST', '/api/orders').as('createOrder');
cy.get('[data-cy=place-order]').click();
cy.wait('@createOrder').then(({ request, response }) => {
  expect(request.body).to.deep.include({ sku: 'SKU-1', qty: 2 });
  expect(response.statusCode).to.eq(201);
});
cy.get('[data-cy=confirmation]').should('contain', 'Order placed');
```
Shorthand assertions: `cy.wait('@createOrder').its('response.statusCode').should('eq', 201)`.

## Register before triggering
`cy.intercept` must be called before the action (or `cy.visit`) that fires the request.

## Multiple requests
```js
cy.wait(['@me', '@flags', '@basket']);                  // waits for each once
cy.wait('@search'); cy.wait('@search');                 // second call of same alias
cy.get('@search.all').should('have.length', 2);         // all matched calls so far
cy.wait('@search').its('request.url').should('include', 'q=beans');
```
Each `cy.wait('@alias')` consumes the next unmatched request for that alias.

## Timeouts
- `requestTimeout` (5 s) waits for the request to go out; `responseTimeout` (30 s) waits for the response.
- Override per call: `cy.wait('@report', { timeout: 60000 })`.

## Matching
Use `RouteMatcher` objects for precision: `cy.intercept({ method: 'GET', pathname: '/api/orders', query: { status: 'open' } })`. Glob `**` and regex also supported.

## Gotchas
- Waiting on an alias for a request already finished before the wait is fine (it was recorded), but registering the intercept after it fired is not.
- `cy.wait(2000)` is never the fix.

## Verify
Run on Cypress 16.2.0: `cy.wait` on one and several aliases, repeated waits consuming successive requests, `@alias.all`, RouteMatcher `pathname` + `query`, glob and regex matching, request-body assertions, and the "No request ever occurred" timeout error (also when the intercept was registered after the request fired). Tests contain no numeric `cy.wait`, and assertions on request bodies catch a frontend payload regression.
