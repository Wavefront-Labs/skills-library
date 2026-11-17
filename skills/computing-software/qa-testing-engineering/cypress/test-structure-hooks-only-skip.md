---
id: computing-software.qa-testing-engineering.cypress.test-structure-hooks-only-skip
name: test-structure-hooks-only-skip
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-hooks, mocha-hooks, describe-it, only-skip, test-configuration]
level: practitioner
status: verified
description: "Structure Cypress specs with Mocha describe/context/it, before/beforeEach/after hooks, .only/.skip, per-test configuration and support-file global hooks."
sources:
  - https://docs.cypress.io/app/core-concepts/writing-and-organizing-tests
  - https://docs.cypress.io/app/references/configuration#Test-Configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test structure, hooks, only and skip

```js
describe('Checkout', { tags: '@smoke' }, () => {
  before(() => { cy.task('db:seed') });             // once per spec file
  beforeEach(() => { cy.login(); cy.visit('/cart') }); // before every test
  afterEach(function () { if (this.currentTest.state === 'failed') cy.task('log', this.currentTest.title) });

  context('with items', () => {
    it('shows total', () => { cy.get('[data-cy=total]').should('contain', '$') });
    it.skip('applies coupon', () => {});
    it('pays', { retries: 2, viewportWidth: 375 }, () => { ... });
  });
});
```

## Where hooks go
- Spec-level: inside `describe`.
- Global (every spec): `cypress/support/e2e.js` top-level `beforeEach`.
- Avoid `after`/`afterEach` for cleanup of state the next test depends on: if the test runner crashes, cleanup never runs. Reset state in `beforeEach` instead (Cypress best practice).

## .only / .skip
`it.only` / `describe.only` run just those, in `cypress run` as well as `cypress open` (a 16.2.0 `run` executed only the `.only` test). Do not commit: `eslint-plugin-mocha` `no-exclusive-tests`, or `@cypress/grep` with tags for selection instead.

## Test isolation
With `testIsolation: true` (default since v12), Cypress clears cookies, localStorage, sessionStorage and visits `about:blank` before each test, so `beforeEach` must re-establish state (use `cy.session` to keep it cheap).

## Tag filtering
`@cypress/grep` (7.0.0 on npm; needs `register()` from `@cypress/grep` in the support file and `plugin(config)` from `@cypress/grep/plugin` in `setupNodeEvents`): on Cypress 16 pass the filters as exposed values, `npx cypress run --expose grepTags=@smoke,grepFilterSpecs=true`. With the plugin loaded, `--expose grepTags=@smoke,grepFilterSpecs=true` ran 1 of 2 specs; `--env grepTags=...` filtered nothing. Without the plugin, `{ tags: '@smoke' }` in the suite config is accepted and ignored (all tests ran).

## Gotchas
- `before` failing skips all tests in the block, reported as one failure (`"before all" hook for "shows total"`; sibling `describe` blocks still ran).
- Arrow functions lose `this.currentTest`; use `function`.

## Verify
Run on Cypress 16.2.0: hook order, `this.currentTest.state` in `afterEach` (`failed` / `passed`), `it.skip`, per-test `retries`/`viewportWidth` overrides, and the `before` failure above. Running a single test with `.only` locally passes alone (no hidden dependency on earlier tests).
