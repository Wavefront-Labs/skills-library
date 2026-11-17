---
id: computing-software.qa-testing-engineering.cypress.session-validate-and-cache-across-specs
name: session-validate-and-cache-across-specs
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cacheacrossspecs, cy-session, session-validation, cypress-login]
level: practitioner
status: verified
description: "Cache Cypress logins with cy.session using validate callbacks, cacheAcrossSpecs, unique session ids per role, and debugging session restore failures."
sources:
  - https://docs.cypress.io/api/commands/session
  - https://docs.cypress.io/app/guides/authentication-testing/social-authentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cy.session validate and cacheAcrossSpecs

```js
Cypress.Commands.add('login', (role = 'admin') => {
  cy.session([role], () => {
    cy.env([`${role}_user`, `${role}_pass`])      // Cypress 16: Cypress.env() was removed
      .then((c) => cy.request('POST', '/api/login', { user: c[`${role}_user`], pass: c[`${role}_pass`] }))
      .its('body.token').then(t => window.localStorage.setItem('token', t));
  }, {
    validate() {
      cy.request({ url: '/api/me', headers: { authorization: `Bearer ${localStorage.getItem('token')}` } })
        .its('status').should('eq', 200);
    },
    cacheAcrossSpecs: true,
  });
});
```

## How it works
- First call: runs setup, then validate, then snapshots cookies, localStorage, sessionStorage for all domains.
- Next calls with the same id: clear page, restore snapshot, run validate. If validate fails, setup runs again once.
- `cacheAcrossSpecs: true` keeps the session for the whole `cypress run` (not just the spec). Default false.
- Ids can be any serialisable value; include everything that changes the session (role, tenant).

## After cy.session
The page is `about:blank`; always `cy.visit()` after `cy.login()`.

## Debugging
Command log shows "Session (new)", "(saved)", "(recreated)". Click it to see restored storage. `Cypress.session.clearAllSavedSessions()` resets during `cypress open`.

## Gotchas
- HttpOnly cookies set by the server are captured; tokens kept only in memory (JS variables) are not: the app must re-hydrate from storage.
- Validate must actually prove the session works (call a protected endpoint), not just check that a cookie exists.
- Changing the setup function code does not invalidate a cached session in open mode; change the id or clear.
- Calling `cy.session` with an id already used in the run but a different setup or validate function throws "This session already exists. You may not create a new session with a previously used identifier" (hit in a 16.2.0 run); wrap one `cy.session` in a shared command, as above.
- A `validate` that still fails right after setup fails the test ("validation failed immediately after creating the session").

## Verify
Run on Cypress 16.2.0: setup then validate; page `about:blank` after `cy.session`; restore in the next test and in a second spec with `cacheAcrossSpecs` (one setup for `admin` across two specs, a separate one for `editor`); a validate that failed on restore re-ran setup (2 setups, 3 validate calls); `Cypress.session.clearAllSavedSessions` is a function. Second test's log shows the session restored in ms, and logged-in UI renders.
