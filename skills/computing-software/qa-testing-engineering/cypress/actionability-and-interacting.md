---
id: computing-software.qa-testing-engineering.cypress.actionability-and-interacting
name: actionability-and-interacting
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-actionability, cypress-click, force-option, scrollbehavior, cy-type]
level: practitioner
status: verified
description: "Interact with elements in Cypress knowing its actionability checks (visible, not disabled, not covered, not animating), scrollBehavior, force: true trade-offs and cy.type keys."
sources:
  - https://docs.cypress.io/app/core-concepts/interacting-with-elements
  - https://docs.cypress.io/api/commands/type
  - https://docs.cypress.io/api/commands/click
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interacting with elements and actionability

## What Cypress checks before an action
1. Scroll element into view (`scrollBehavior`: `top` default, `center`, `bottom`, `nearest`, `false`; Cypress 16 also accepts an object such as `{ block: 'center', inline: 'nearest' }`).
2. Not hidden. Cypress 16 defaults to `visibilityStrategy: 'modern'` (browser `Element.checkVisibility()`): zero width/height, `display: none` on the element or an ancestor, `visibility: hidden|collapse`, `content-visibility: hidden`, `opacity: 0` (when asserting visibility). The deprecated `'legacy'` strategy also treated overflow-clipped, scrolled-out and covered `fixed`/`sticky` elements as hidden.
3. Not disabled, not detached, not readonly (a readonly input fails `type`: "failed because this element is readonly"; a disabled one: "...is `disabled`").
4. Not animating (`animationDistanceThreshold` default 5, `waitForAnimations` default true).
5. Not covered: the element at the click coordinates must be the target or a descendant.
Then it fires the event chain (pointerdown, mousedown, focus, pointerup, mouseup, click).

## Common commands
```js
cy.get('[data-cy=email]').type('a@b.test{enter}');
cy.get('[data-cy=email]').clear().type('x', { delay: 0 });
cy.get('[data-cy=agree]').check(); cy.get('select').select('NZ');
cy.get('[data-cy=menu]').trigger('mouseover');   // no native hover in Cypress
cy.get('body').type('{ctrl+k}');
cy.get('[data-cy=card]').click('topRight');
```
Special keys: `{enter}`, `{esc}`, `{backspace}`, `{selectall}`, `{moveToEnd}`, modifiers `{shift}`, `{alt}`. Real native events (e.g. true hover) need `cypress-real-events` (Chromium only).

## force: true
Skips all checks except existence and fires events anyway. Legit: custom inputs visually hidden behind a label. Otherwise it masks bugs (overlay covering the button in production).

## Reading errors
`cy.click() failed because this element is being covered by another element: <div class="modal-backdrop">` -> wait for the modal to close (`cy.get('.modal-backdrop').should('not.exist')`).

## Gotchas
- `cy.type` into a field with an input mask may drop characters: raise the delay (`{ delay: 10 }` or `keystrokeDelay`; the default `keystrokeDelay` changed from 10 to 0 in Cypress 16.0.0) or set value then trigger `input`.
- `scrollBehavior` centre helps with sticky headers covering elements scrolled to the top.

## Verify
Checked on Cypress 16.2.0 (Electron): `type` with `{enter}`, `{ctrl+k}`, `clear`, `click('topRight')`, `click({force:true})`, and the multi-element click error all behave as listed. No `force: true` without a comment; covered-element errors fixed at the cause.
