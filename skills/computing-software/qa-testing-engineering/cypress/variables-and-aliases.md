---
id: computing-software.qa-testing-engineering.cypress.variables-and-aliases
name: variables-and-aliases
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-aliases, cy-wrap, cypress-then, cypress-core-concepts, command-chaining]
level: practitioner
status: verified
description: "Share values in Cypress the right way: why const assignment fails, .then() closures, .as() aliases with this.* and cy.get('@alias'), cy.wrap, and alias types."
sources:
  - https://docs.cypress.io/app/core-concepts/variables-and-aliases
  - https://docs.cypress.io/api/commands/as
  - https://docs.cypress.io/api/commands/wrap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables and aliases in Cypress (as, then, wrap)

**Goal:** use values yielded by commands without fighting Cypress's asynchronous command queue.

## Why `const x = cy.get(...)` does not work
Commands are enqueued and run later; they return chainers, not values. A plain `let` assigned inside `.then()` is not set when the next line of test code runs (only when the queue reaches it).

## .then() closures
```js
cy.get('[data-cy=order-id]').invoke('text').then((orderId) => {
  cy.visit(`/orders/${orderId}`);
  cy.contains('h1', orderId);
});
```

## Aliases
```js
cy.get('[data-cy=basket-row]').as('rows');
cy.get('@rows').should('have.length', 3);          // re-queries the DOM (query alias)

cy.intercept('GET', '/api/orders*').as('orders');  // route alias, see cy.wait
cy.fixture('user.json').as('user');                // value alias

it('uses this context', function () {               // function(), not arrow, for this.*
  cy.request('/api/me').its('body.id').as('userId');
  cy.then(function () { expect(this.userId).to.be.a('number'); });
});
```
- Aliases reset before each test; define them in `beforeEach`.
- `.as('name', { type: 'static' })` stores the value once instead of re-running the query (option added in Cypress 12.4.0; since 12.0.0 aliases re-run their queries by default).
- `this.alias` only works for values aliased before the current command and inside `function` callbacks.

## cy.wrap
Bring a value or promise into the chain:
```js
cy.wrap({ total: 36 }).its('total').should('eq', 36);
cy.wrap(apiClient.createOrder()).then((order) => cy.visit(`/orders/${order.id}`)); // waits for promise
cy.wrap($el).click();          // jQuery element from a .then callback
```

## Gotchas
- Mixing async/await with Cypress commands does not work; commands are not promises.
- Returning a value from `.then` that is `undefined` yields the previous subject; return explicitly.

## Verify
Run on Cypress 16.2.0: `invoke('text').as(...)` read via `cy.get('@t')` and `this.t`, a query alias asserted with `cy.get('@rows').should('have.length', 3)`, a static alias, `cy.wrap` with a promise and with an object, and `.then` returning `undefined` (subject kept) versus a value. No test reads values assigned outside the queue, and aliases are created in hooks or before use in the same test.
