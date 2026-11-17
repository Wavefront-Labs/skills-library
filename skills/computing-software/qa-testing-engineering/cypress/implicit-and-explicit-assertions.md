---
id: computing-software.qa-testing-engineering.cypress.implicit-and-explicit-assertions
name: implicit-and-explicit-assertions
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-should, cypress-assertions, chai-assertions, retry-ability, implicit-assertions]
level: practitioner
status: verified
description: "Write Cypress assertions that retry: implicit .should and .and chains, callback should with expect, explicit expect in .then (no retry), and default existence checks."
sources:
  - https://docs.cypress.io/app/references/assertions
  - https://docs.cypress.io/api/commands/should
  - https://docs.cypress.io/app/core-concepts/retry-ability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit vs explicit assertions (should, expect)

## Implicit (retrying) assertions
```js
cy.get('[data-cy=total]').should('have.text', '£36.00');
cy.get('[data-cy=rows]').should('have.length', 3).and('be.visible');
cy.get('input[name=email]').should('have.value', 'a@example.test').and('have.attr', 'aria-invalid', 'false');
cy.url().should('include', '/orders/');
cy.get('[data-cy=spinner]').should('not.exist');
```
The query before `.should` is retried until all chained assertions pass or the timeout (`defaultCommandTimeout`, 4 s) expires.

## Callback should (retrying, multiple checks)
```js
cy.get('[data-cy=price]').should(($els) => {
  const prices = [...$els].map((el) => parseFloat(el.innerText.replace('£', '')));
  expect(prices).to.deep.equal([...prices].sort((a, b) => a - b));   // sorted ascending
});
```
The callback must be idempotent (no side effects; it runs many times).

## Explicit (no retry)
```js
cy.get('[data-cy=total]').then(($el) => {
  expect($el.text()).to.equal('£36.00');     // evaluated once
});
```
Use `.then` + `expect` only for values that are already stable, or wrap them with `cy.wrap(value).should(...)`.

## Default assertions
Most queries implicitly assert existence (`cy.get` waits for the element); actions also wait for actionability (visible, not disabled, not covered). `.should('not.exist')` replaces the default.

## Common chainers
`have.text`, `contain` / `contain.text`, `have.value`, `have.class`, `have.attr`, `have.css`, `be.visible`, `be.disabled`, `be.checked`, `have.length.gte`, and `match`: on a string subject it takes a regex (`cy.get('h1').invoke('text').should('match', /^Hel/)`), on elements it takes a selector (`.should('match', 'h1')`; a regex against an element fails with "expected '<h1>' to match").

## Gotchas
- Asserting on a stale chain: `cy.get('li').first().should(...)` retries the whole query chain since Cypress 12.
- `.should('be.visible')` on elements under a sticky header can pass while clicking still fails (covered); check the action error.

## Verify
The chainers above, the callback `should`, `not.exist` and the default `cy.get` existence wait (it failed with "Expected to find element" after the timeout) were run on Cypress 16.2.0. Assertions about async UI use `should`, `then`+`expect` only appear for stable values, and no `cy.wait(ms)` is needed for timing.
