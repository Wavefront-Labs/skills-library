---
id: computing-software.qa-testing-engineering.cypress.within-shadow-dom-and-iframes
name: within-shadow-dom-and-iframes
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-iframe, includeshadowdom, shadow-dom, cypress-within, cypress-core-concepts]
level: practitioner
status: verified
description: "Scope Cypress queries with within(), reach into shadow DOM via shadow() and includeShadowDom, and work with iframes through the iframe document body."
sources:
  - https://docs.cypress.io/api/commands/within
  - https://docs.cypress.io/api/commands/shadow
  - https://www.cypress.io/blog/working-with-iframes-in-cypress
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# within, shadow DOM and iframes in Cypress

## within
```js
cy.get('[data-cy=shipping-form]').within(() => {
  cy.get('input[name=postcode]').type('SW1A 1AA');
  cy.contains('button', 'Save').click();
});
```
Inside `within`, `cy.get` is scoped; use `cy.root()` for the scope element. To query outside the scope for one command: `cy.get('body', { withinSubject: null })`.

## Shadow DOM
```js
cy.get('my-date-picker').shadow().find('button.next-month').click();
cy.get('.next-month', { includeShadowDom: true }).click();
```
Global: `includeShadowDom: true` in `cypress.config.js` or test config (applies to get, find, contains; default false; worked as a test-config override on 16.2.0). Open shadow roots only: a `{ mode: 'closed' }` root was not found even with `includeShadowDom`.

## iframes
Cypress has no built-in `cy.iframe`; access the iframe's document once loaded:
```js
const getIframeBody = () =>
  cy.get('iframe[data-cy=payment-frame]')
    .its('0.contentDocument.body').should('not.be.empty')   // retries until loaded
    .then(cy.wrap);

getIframeBody().find('input[name=cardnumber]').type('4242424242424242');
```
Make it a custom command (`Cypress.Commands.add('iframeBody', ...)`) or use the `cypress-iframe` plugin (`cy.frameLoaded()`, `cy.iframe()`).

## Limits
- Cross-origin iframes (e.g. Stripe Elements, third-party widgets) are blocked by the browser's same-origin policy: `its('0.contentDocument.body')` on a `127.0.0.1:3457` frame inside a `localhost:3456` page failed with "does not exist on your subject", and passed with `chromeWebSecurity: false` (Electron; the option is Chromium-only per the config docs) or stub the provider in test mode.
- `cy.intercept` saw a `fetch` made from inside an iframe.

## Gotchas
- Querying the iframe body before it loads returns an empty body; the `.should('not.be.empty')` retry is essential.
- `within` with a subject that matches multiple elements errors; scope to one.

## Verify
Run on Cypress 16.2.0: `within` (scoped `cy.get`, `cy.root()`, `withinSubject: null`, the multi-element error), `.shadow()`, `includeShadowDom`, and the iframe body pattern with `.then(cy.wrap)`. Iframe and shadow interactions pass repeatedly with no fixed waits, and the cross-origin approach is documented per third-party widget.
