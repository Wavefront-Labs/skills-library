---
id: computing-software.qa-testing-engineering.cypress.typing-custom-commands-typescript
name: typing-custom-commands-typescript
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-typescript, custom-commands, typescript, cypress-config, type-declarations]
level: practitioner
status: verified
description: "Use TypeScript in Cypress: tsconfig for the cypress folder, declaring custom command types on Cypress.Chainable, typed fixtures and avoiding global type clashes with Jest."
sources:
  - https://docs.cypress.io/app/tooling/typescript-support
  - https://docs.cypress.io/api/cypress-api/custom-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typing custom commands in TypeScript (Cypress)

## Setup
Cypress compiles TS out of the box when `typescript` is installed. Add `cypress/tsconfig.json`:
```json
{
  "compilerOptions": { "target": "es2020", "lib": ["es2020", "dom"], "types": ["cypress", "node"], "strict": true },
  "include": ["**/*.ts", "../cypress.config.ts"]
}
```
A separate `cypress/tsconfig.json` with `"types": ["cypress", "node"]` limits the global types the Cypress files see, so other frameworks' globals (for example Jest's `expect`) do not collide with Chai's.

## Declare and implement a command
```ts
// cypress/support/commands.ts
declare global {
  namespace Cypress {
    interface Chainable {
      /** Log in through the API and cache the session. */
      login(email: string, password?: string): Chainable<void>;
      getByCy(selector: string, options?: Partial<Loggable & Timeoutable>): Chainable<JQuery<HTMLElement>>;
    }
  }
}

Cypress.Commands.add('login', (email, password) => {
  cy.session(email, () => {
    cy.env(['PW']).then(({ PW }) => {   // Cypress 16: Cypress.env() was removed; cy.env() reads secrets
      cy.request('POST', '/api/login', { email, password: password ?? PW });
    });
  });
});
Cypress.Commands.add('getByCy', (selector, options) => cy.get(`[data-cy="${selector}"]`, options));

export {};   // make the file a module so declare global works
```
Import it from `cypress/support/e2e.ts`.

## Child commands (with a subject)
```ts
interface Chainable<Subject> { shouldHaveMoney(amount: number): Chainable<Subject>; }
Cypress.Commands.add('shouldHaveMoney', { prevSubject: 'element' }, (subject, amount) => {
  cy.wrap(subject).should('have.text', `£${amount.toFixed(2)}`);
});
```

## Typed fixtures and intercept bodies
```ts
import type { Order } from '../../src/types';
cy.fixture<Order>('order.json').then((order) => { /* typed */ });
cy.wait('@createOrder').its('response.body').then((body: Order) => { ... });
```

## Gotchas
- Missing `export {}` makes declarations silently not apply.
- Overwriting built-ins: `Cypress.Commands.overwrite<'type', 'element'>('type', (orig, el, text, opts) => ...)`.
- Editors need the cypress tsconfig in scope; open the project root.

## Verify
Run on Cypress 16.2.0 with TypeScript 7.0.2: `npx tsc -p cypress --noEmit` passed for the files above plus a spec using `login`, `getByCy`, `shouldHaveMoney` and typed fixture/intercept bodies, and `cypress run` executed that `.ts` spec. Dropping `export {}` made `tsc` report `getByCy`/`login` missing and "Augmentations for the global scope can only be directly nested in external modules". `npx tsc -p cypress --noEmit` passes in CI and custom commands autocomplete with JSDoc.
