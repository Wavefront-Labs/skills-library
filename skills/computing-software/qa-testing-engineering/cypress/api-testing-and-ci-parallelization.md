---
id: computing-software.qa-testing-engineering.cypress.api-testing-and-ci-parallelization
name: api-testing-and-ci-parallelization
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress, api-testing, cy-request, contract-checks, schema-validation, json-schema, ci, parallelization, sharding, matrix-build, github-actions, cypress-cloud, test-splitting, flaky-tests, headless, cy-pipe, backend-testing]
level: practitioner
status: verified
description: "Use Cypress as an API testing tool with cy.request/cy.api, validate response schemas, and split a growing suite across CI machines without a paid orchestrator."
sources: ["https://docs.cypress.io/api/commands/request", "https://docs.cypress.io/guides/guides/parallelization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cypress as an API test runner, and splitting the suite across CI

**Goal:** use Cypress's `cy.request` to test a backend directly (faster and more
stable than driving it through the UI), and run the resulting suite — UI and API —
fast on CI by splitting it across machines correctly.

## 1. API tests with cy.request
`cy.request` bypasses the browser's same-origin and CORS restrictions (it runs in
Node), so it is the right tool for backend contract checks that don't need a DOM:
```js
cy.request('POST', '/api/orders', { sku: 'A1', qty: 2 }).then((res) => {
  expect(res.status).to.eq(201)
  expect(res.body).to.have.property('id')
  expect(res.body.total).to.eq(2 * 19.99)
})
```
Unlike `cy.intercept`, `cy.request` does **not** retry on failed assertions inside
`.then()` — if the assertion can race the server, wrap the check in `cy.wrap().should()`
instead of a bare `.then()` callback, or poll explicitly.

## 2. Schema validation, not just field checks
Field-by-field assertions miss additive/structural drift. Validate against a JSON
Schema instead, so the test fails when the contract changes shape, not just values:
```js
import Ajv from 'ajv'
const ajv = new Ajv()
const valid = ajv.validate(orderSchema, res.body)
expect(valid, JSON.stringify(ajv.errors)).to.be.true
```
Keep the schema in the repo next to the test (or generated from the backend's
OpenAPI spec) so it's reviewed in the same PR as a real API change.

## 3. Auth for API tests
Get a token once via `cy.request('POST', '/auth/login', creds)` in a custom command,
cache it with `cy.session()`, and attach it as a header on subsequent `cy.request`
calls — never re-authenticate per test. This is also the fastest way to seed state
for UI tests: create the fixture data via API request, then `cy.visit()` straight to
the screen under test instead of clicking through a wizard.

## 4. Splitting the suite on CI without a paid dashboard
Cypress Cloud's `--parallel` flag (which the CLI only accepts together with `--record`) is what load-balances specs
dynamically; pricing/plan details are not covered here. Without it, split manually by **spec count**, not file size, across
N matrix jobs — a simple round-robin glob split keeps jobs balanced better than a
hand-picked split that drifts as specs are added:
```yaml
strategy:
  matrix: { shard: [1, 2, 3, 4] }
steps:
  - run: |
      SPECS=$(find cypress/e2e -name '*.cy.js' | sort | awk -v n=4 -v s=${{ matrix.shard }} 'NR % n == s - 1' | paste -sd, -)
      npx cypress run --spec "$SPECS"
```
The earlier `ls cypress/e2e/**/*.cy.js | tr '\n' ','` form was wrong in two ways, both reproduced locally: in a default (non-globstar) bash `**` behaves like `*`, so top-level specs were silently dropped (4 of 7 files listed), and the trailing comma makes Cypress exit with "Expected pattern to be a non-empty string". `find ... | sort | paste -sd, -` listed all 7 across the 4 shards with no trailing comma, and `--spec "a.cy.js,b.cy.js"` ran both. (Running the generated command on GitHub Actions was not possible here.)
Separate API-only specs into their own CI job — they never render the app so they run in
a fraction of the time (Cypress still starts a browser for each spec) and shouldn't share a timeout budget with UI specs.

## 5. Common mistake
Don't use `cy.request` to replace UI assertions on UI behavior ("the button is
disabled") — that's testing the API, not the thing the user sees. Use it to set up
state and to test the backend contract directly; use `cy.visit`/`cy.get` for what
the user actually experiences.

## Notes
Run on Cypress 16.2.0 locally: `cy.request` against a local server (status, body property, no CORS needed), the Ajv schema check (Ajv 8), and the sharding shell above. Cypress Cloud parallelization (`--parallel` needs `--record`; the CLI rejects it otherwise) is not covered; the manual sharding approach is dashboard-independent.

## Verify
- [ ] API tests validate response shape (schema), not only a few fields.
- [ ] Auth token fetched once per run/session, not per test.
- [ ] API-only specs run in a separate, faster CI job than UI specs.
- [ ] Manual CI shards stay balanced as specs are added (spec-count split, not static list).
- [ ] No `cy.request` assertion races the server inside an unwrapped `.then()`.
