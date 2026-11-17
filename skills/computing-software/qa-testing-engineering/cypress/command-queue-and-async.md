---
id: computing-software.qa-testing-engineering.cypress.command-queue-and-async
name: command-queue-and-async
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [command-queue, cypress-async, cy-then, chainable, cypress-variables]
level: practitioner
status: verified
description: "Understand Cypress's enqueued command model: why commands are not promises, avoiding async/await and sync variable reads, and using .then, aliases and closures correctly."
sources:
  - https://docs.cypress.io/app/core-concepts/introduction-to-cypress#Commands-Are-Asynchronous
  - https://docs.cypress.io/app/core-concepts/variables-and-aliases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command queue asynchrony

## The model
`cy.*` calls **enqueue** commands and return immediately; Cypress runs the queue after the test function returns. So:
```js
let text;
cy.get('h1').then($h => { text = $h.text(); });
console.log(text);                 // undefined: runs before the queue
cy.then(() => console.log(text));  // correct: runs in the queue
```

## Don'ts
```js
const el = cy.get('h1');           // a Chainable, not an element
await cy.get('h1');                // Chainables are not promises: fails with "Cypress test was stopped while running this command" (16.2.0)
if (cy.get('.x')) { ... }          // always truthy, and the cy.get still runs and fails if .x is absent
```
Do not return a promise and also issue cy commands in the same `.then`; return the cy chain (or the promise) but not both. A quick 16.2.0 run of that mix did not throw, so the order of work is not something to rely on.

## Do
```js
cy.get('[data-cy=total]').invoke('text').then(parseFloat).should('be.gt', 0);
cy.get('[data-cy=id]').invoke('text').as('orderId');
cy.get('@orderId').then(id => cy.visit(`/orders/${id}`));
// Reading values in `function` callbacks via this.* (aliases on the test context)
beforeEach(function () { cy.fixture('user').as('user'); });
it('logs in', function () { cy.login(this.user.email); });
```
Wrapping async work: `cy.wrap(fetchToken())` waits for the promise and yields its value.

## Synchronous code between commands
Plain JS runs at enqueue time. Put it inside `.then()` if it depends on earlier commands.

## Gotchas
- `this.*` aliases need `function () {}`, not arrow functions.
- Returning a different value from `.then` changes the subject; returning `undefined` keeps it.
- Loops with `cy` commands enqueue all iterations up front; recursion via `.then` for "until" logic (bounded).

## Verify
Sync-vs-queue ordering, `.then` returning `undefined`, `cy.wrap(promise)`, `this.alias` in `function` callbacks (undefined with arrows) and loop enqueueing (`out=[]` right after the loop, `[0,1,2]` once the queue ran) were all run on Cypress 16.2.0. No `await cy` in the codebase (`eslint-plugin-cypress` has rules for unsafe chaining and async tests).
