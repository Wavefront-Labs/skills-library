---
id: computing-software.qa-testing-engineering.cypress.cookies-and-local-storage
name: cookies-and-local-storage
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-setcookie, cy-getcookie, cypress-localstorage, cy-clearcookies, cookie-testing]
level: practitioner
status: verified
description: "Read, set and clear cookies and web storage in Cypress (setCookie, getCookie, getAllCookies, clearAllLocalStorage) and test cookie flags and consent banners."
sources:
  - https://docs.cypress.io/api/commands/setcookie
  - https://docs.cypress.io/api/commands/getcookie
  - https://docs.cypress.io/api/commands/clearalllocalstorage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cookies and localStorage handling

## Cookies
```js
cy.setCookie('consent', 'all', { domain: '.example.test', secure: true, sameSite: 'lax' });
cy.getCookie('session').should('exist').and('have.property', 'httpOnly', true);
cy.getCookie('session').its('secure').should('eq', true);
cy.getCookies().should('have.length.greaterThan', 0);   // current domain
cy.getAllCookies();                                      // all domains
cy.clearCookie('consent'); cy.clearAllCookies();
```
`domain` option reads cookies for other domains; cross-origin pages still need `cy.origin` to interact.
Since Cypress 16.0.0 `cy.getCookie`, `cy.getCookies`, `cy.getAllCookies`, `cy.getAllLocalStorage` and `cy.getAllSessionStorage` are query commands: attached assertions retry (a cookie set 1 s later satisfied `cy.getCookie('late').should('exist')`), the timeout follows `defaultCommandTimeout`, and overwriting them needs `Cypress.Commands.overwriteQuery()` (`Commands.overwrite` throws "Queries can only be overwritten with `Cypress.Commands.overwriteQuery()`").

## Storage
```js
cy.window().then(win => win.localStorage.setItem('featureFlags', JSON.stringify({ newNav: true })));
cy.visit('/', { onBeforeLoad(win) { win.localStorage.setItem('tour-done', '1'); } });  // before app boots
cy.getAllLocalStorage().then(all => expect(all['http://localhost:3000']).to.have.property('token'));
cy.clearAllLocalStorage(); cy.clearAllSessionStorage();
```

## Typical tests
- Session cookie flags: `HttpOnly`, `Secure`, `SameSite`, sensible expiry.
- Consent: pre-set the consent cookie to skip the banner in most tests; one test covers the banner itself.
- Logout clears session cookie and storage; back button does not restore an authenticated page.

## Gotchas
- Test isolation clears cookies/storage between tests (v12+); set them in `beforeEach` or via `cy.session`.
- Setting storage after `cy.visit` is too late for apps that read it on boot: use `onBeforeLoad`.
- `Secure` cookies need https in general; a `secure: true` cookie was set and read back on `http://localhost` (Electron), the only host tried.

## Verify
Run on Cypress 16.2.0 against a local server: `httpOnly`/`sameSite` assertions, `getAllCookies` listing other domains, `getAllLocalStorage` keyed by origin, `onBeforeLoad` storage, and storage/cookies empty at the start of the next test (test isolation). Cookie flag assertions fail when the server drops `HttpOnly`.
