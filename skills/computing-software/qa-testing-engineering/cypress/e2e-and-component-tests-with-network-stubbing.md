---
id: computing-software.qa-testing-engineering.cypress.e2e-and-component-tests-with-network-stubbing
name: e2e-and-component-tests-with-network-stubbing
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress, e2e-testing, end-to-end, component-testing, cy-intercept, network-stubbing, fixtures, retry-ability, command-chaining, aliases, cy-session, custom-commands, data-cy, cypress-config, headless, cypress-run, cypress-open, react, vue, javascript, typescript, flaky-tests, ci, front-end-testing]
level: practitioner
status: verified
description: "Cypress E2E and component tests that don't flake: understand the command queue and retry-ability, stub or wait on network with cy.intercept, cache setup with cy.session, run in CI."
sources: ["https://docs.cypress.io/app/core-concepts/introduction-to-cypress", "https://docs.cypress.io/api/commands/intercept", "https://docs.cypress.io/app/core-concepts/best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cypress: E2E and component tests with controlled network

**Goal:** Cypress tests that read like user stories, run deterministically by
controlling or waiting on the network, and pass the same way in `cypress run` on CI.

## 1. Setup and the two runners
```bash
npm i -D cypress
npx cypress open    # interactive: choose E2E or Component Testing; scaffolds cypress.config.ts
npx cypress run --browser chrome          # headless, for CI (default is Electron, deprecated since 16; `--browser edge` also worked here)
npx cypress run --component               # component tests only
```
Minimal `cypress.config.ts`:
```ts
import { defineConfig } from 'cypress'
export default defineConfig({
  e2e: { baseUrl: 'http://localhost:3000', retries: { runMode: 2, openMode: 0 } },
  component: { devServer: { framework: 'react', bundler: 'vite' } },
})
```
Set `baseUrl` (the prefix for `cy.visit()` and `cy.request()`); then `cy.visit('/cart')`.
Component testing with Vite also needs a Vite config file found upwards from the project (without one, `cypress run --component` stops with "a configuration file was not found"), and Cypress 16 requires Vite 8 or newer (React/vite plugin). `cy.mount` is not built in: register it in `cypress/support/component.tsx` (`Cypress.Commands.add('mount', mount)` with `import { mount } from 'cypress/react'`, or a wrapper: see mounting-components-with-providers).

## 2. The mental model you must have
Cypress commands are **enqueued, not executed** when the line runs. So this is wrong:
```js
const text = cy.get('h1').invoke('text')   // a chainable, NOT a string
```
Use `.then()` for values, or better, assert directly. **Queries and assertions retry**
together until `defaultCommandTimeout` (4 s): `cy.get('[data-cy=total]').should('have.text', '$42.00')`
re-queries the DOM until it matches. Actions (`.click()`, `.type()`) do not retry.
Gotcha: only the *last query* before `.should` retries. Prefer
`cy.get('[data-cy=row]').should('have.length', 3)` over splitting a query and an
assertion across `.then()` callbacks, which breaks retry.

## 3. Selectors
Use dedicated attributes: `cy.get('[data-cy=submit]')`. `cy.contains('button', 'Pay now')`
is fine when the text is the requirement. Avoid CSS classes and tag positions.

## 4. Network: wait on it or stub it with cy.intercept
**Wait for the real call** (instead of `cy.wait(2000)`):
```js
cy.intercept('POST', '/api/orders').as('createOrder')
cy.get('[data-cy=pay]').click()
cy.wait('@createOrder').its('response.statusCode').should('eq', 201)
```
Register the intercept **before** the action that triggers it, or the request is missed.

**Stub the response** to test UI states that are hard to produce for real:
```js
cy.intercept('GET', '/api/products*', { fixture: 'products.json' }).as('products')   // cypress/fixtures/
cy.intercept('GET', '/api/products*', { statusCode: 500, body: { error: 'boom' } })
cy.intercept('GET', '/api/products*', { delay: 3000, fixture: 'products.json' })     // spinner state
```
Strategy: stub heavily in component and most E2E UI tests; keep a small set of
un-stubbed "smoke" E2E tests against a real backend so contract drift is caught.

## 5. Setup without the UI
- Seed and reset data via API or a task, not by clicking: `cy.request('POST', '/test/reset')`
  or `cy.task('db:seed')` (tasks run in Node, defined in `setupNodeEvents`).
- Cache login per spec run with `cy.session(id, setupFn, { validate })`; the session is
  restored for later tests. Do the actual sign-in through an API request in the setup
  function where the app allows it, with test-account values read through `cy.env()` (Cypress 16 removed `Cypress.env()`)
  and supplied by CI secrets, never committed.
- Reset state in `beforeEach`, not `afterEach` — `afterEach` doesn't run if you stop a
  run midway, so the next run inherits dirty state.

## 6. Component testing
```tsx
// cy.mount comes from cypress/support/component.tsx (see mounting-components-with-providers)
it('disables Pay while submitting', () => {
  cy.intercept('POST', '/api/orders', { delay: 500, statusCode: 201, body: {} })
  cy.mount(<Checkout total={42} />)
  cy.get('[data-cy=pay]').click().should('be.disabled')
})
```
Component tests run the real browser, so CSS and events are real — but you supply
providers (router, store, theme) in a custom `mount` command.

## 7. Known limits
Cypress runs inside the browser and controls one browser at a time: multiple tabs need the `@cypress/puppeteer` plugin per the trade-offs doc (otherwise remove `target=_blank` or assert on the `href`), and navigating to another origin needs `cy.origin()`.
Parallelising across machines is a Cypress Cloud feature; free alternatives split specs per CI job.

## Unconfirmed / notes
Re-checked on Cypress 16.2.0 with Node 22: the intercept, alias, `cy.task`, `cy.session` and component-mount examples ran. `npx cypress open` (interactive) and the Chrome browser were not tried; docs URLs move between versions.

## Verify
- [ ] Zero `cy.wait(<number>)` in the suite; every wait is on an alias.
- [ ] Intercepts registered before the triggering action.
- [ ] Selectors use `data-cy`/`data-testid` or user-visible text.
- [ ] `npx cypress run` passes 5 runs in a row with no retries consumed (check the run summary).
- [ ] An error-state test exists for each critical API (stubbed 500/timeout).
