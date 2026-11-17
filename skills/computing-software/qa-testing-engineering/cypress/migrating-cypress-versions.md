---
id: computing-software.qa-testing-engineering.cypress.migrating-cypress-versions
name: migrating-cypress-versions
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-migration, cypress-upgrade, cypress-config-migration, breaking-changes]
level: practitioner
status: verified
description: "Upgrade Cypress across major versions: config file migration (cypress.json to cypress.config), testIsolation, cy.session, intercept and Node version changes, staged rollout."
sources:
  - https://docs.cypress.io/app/references/migration-guide
  - https://docs.cypress.io/app/references/changelog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating Cypress versions

## Process
1. Read the migration guide and changelog for every major between current and target.
2. Upgrade on a branch: `npm i -D cypress@<target>`; run `npx cypress verify`.
3. Projects older than 10 must go one major at a time: since 15.0 the migration helpers and errors for pre-10 projects are no longer shown. Run `npx cypress verify` after each step (it printed "Verified Cypress!" on 16.2.0).
4. Run the full suite in CI on all browsers; fix failures by category (below).
5. Update Docker images/CI caches and plugin versions together; check each plugin's peer range (`cypress-axe@1.7.0` declares `cypress ^10 ... ^15`, so `npm i` failed with ERESOLVE against Cypress 16 until `--legacy-peer-deps`).

## Notable breaking changes (from the changelog and migration guide)
| Version | Change | Fix |
|---|---|---|
| 10 | `cypress.json` support removed; `cypress.config.{js,ts}` with `e2e`/`component` blocks; `setupNodeEvents` replaces the plugins file | rewrite the config in a `.js`/`.ts` file and set spec and support paths for the new layout |
| 12 | `testIsolation` on by default (clears cookies, localStorage, sessionStorage and visits `about:blank` before each test); `cy.session`/`cy.origin` GA; alias-resolution and query changes; install needs Node 14, 16 or 18+ | re-establish state per test with `cy.session`; convert helpers to `addQuery` |
| 13 | `video` and `videoCompression` default `false`; `videoUploadOnPasses` removed; `cy.readFile` is a query; Node 14 dropped, Node 16 deprecated | set `video: true` if needed |
| 14 | Node 16 and 21 dropped; `cy.origin()` needed for any second origin (scheme, hostname or port) because `document.domain` is no longer injected (`injectDocumentDomain` is the stop-gap); fetch/XHR from `about:blank` in Electron blocked | wrap cross-origin steps in `cy.origin()`; use `cy.request` |
| 15 | Node 18 and 23 dropped (bundled Node 22); `Cypress.SelectorPlayground` renamed `Cypress.ElementSelector`; 3-argument `cy.stub` removed; config loaded with `tsx` | rename the API; use `cy.stub(obj, name).callsFake(fn)` |
| 16 | Requires Node `^22`, `^24` or `>=26`; `Cypress.env()` removed (use `cy.env()` / `Cypress.expose()`), `{ env }` test overrides removed; `cy.exec()` and `execTimeout` removed (use `cy.task`); default `keystrokeDelay` 10 to 0; Vite 8+ for component testing; Chrome/Chromium/Edge use the native browser network (HTTP/2, some `cy.intercept` differences); `cy.getCookie(s)`/`getAllCookies`/`getAllLocalStorage`/`getAllSessionStorage` are queries; Electron deprecated | see https://on.cypress.io/cypress-env-migration; switch browsers; `overwriteQuery` |

Always read the guide for each major between your version and the target; the table is a summary of the headline items.

## Typical failure categories
- Plugin incompatibility: update plugins or replace abandoned ones.
- Tests relying on state from previous tests (exposed by testIsolation).
- Changed behaviours of `cy.intercept` (16: native browser network in Chrome/Chromium/Edge, no `req.httpVersion`, no compression headers on intercepted responses).

## Gotchas
- Upgrade one major at a time for big suites; mixing three majors makes failures hard to attribute.
- Lock the version in CI images and `package.json` (no caret) during the transition.

## Verify
Suite pass rate and duration match the pre-upgrade baseline across browsers.
