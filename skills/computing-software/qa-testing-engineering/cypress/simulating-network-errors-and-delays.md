---
id: computing-software.qa-testing-engineering.cypress.simulating-network-errors-and-delays
name: simulating-network-errors-and-delays
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [forcenetworkerror, network-delay, cy-intercept, error-states, throttle]
level: practitioner
status: verified
description: "Exercise error and loading states in Cypress with cy.intercept forceNetworkError, statusCode stubs, delay and throttleKbps, and req.reply/res.setDelay handlers."
sources:
  - https://docs.cypress.io/api/commands/intercept#StaticResponse-objects
  - https://docs.cypress.io/api/commands/intercept#Response-throttling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simulating network errors and delays

## Static responses
```js
cy.intercept('GET', '/api/orders', { forceNetworkError: true }).as('err');      // connection error
cy.intercept('GET', '/api/orders', { statusCode: 503, body: { message: 'down' } });
cy.intercept('GET', '/api/orders', { statusCode: 200, fixture: 'orders', delay: 2000 }); // loading state
cy.intercept('GET', '/api/big', (req) => { req.on('response', res => res.setThrottle(50)) }); // ~50 kbps
```

## Assert the UX
```js
cy.visit('/orders');
cy.get('[data-cy=spinner]').should('be.visible');
cy.wait('@err');
cy.contains('[role=alert]', 'Could not load orders').should('be.visible');
cy.contains('button', 'Retry').click();
```

## Fail once, then succeed (retry logic)
```js
let calls = 0;
cy.intercept('GET', '/api/orders', (req) => {
  calls += 1;
  if (calls === 1) req.reply({ statusCode: 500 });
  else req.continue();
}).as('orders');
```
Or use `times` option: `cy.intercept({ method: 'GET', url: '/api/orders', times: 1 }, { statusCode: 500 })` registered after the passthrough (newest intercept matches first).

## Gotchas
- `forceNetworkError` makes `fetch` reject with TypeError; XHR fires `error`. Both should map to an error UI.
- Delays add real seconds to the suite; keep them short and only where the loading state is asserted.
- Intercept matching order: last defined wins (a handler that does not reply or continue falls through to older ones); middleware intercepts (`cy.intercept({ url: ..., middleware: true }, handler)`) run first.

## Verify
Run on Cypress 16.2.0: `forceNetworkError` made `fetch` reject with `TypeError` and fired the XHR `error` event; the 503 body, `delay: 1500` (the wait resolved after about 1.5 s), `setThrottle`, the counter version (statuses 500 then 200) and the `times: 1` version (500 then 200) all behaved as listed. Each error state has a test; spinner and retry behaviour are asserted, not just the final happy path.
