---
id: computing-software.qa-testing-engineering.cypress.querying-elements-get-find-contains
name: querying-elements-get-find-contains
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-get, cy-find, cy-contains, data-cy, cypress-selectors]
level: practitioner
status: verified
description: "Query elements in Cypress with cy.get, find, contains and data-cy selectors; understand subject chaining, scoping and the best-practice selector priority."
sources:
  - https://docs.cypress.io/app/core-concepts/introduction-to-cypress#Querying-Elements
  - https://docs.cypress.io/app/core-concepts/best-practices#Selecting-Elements
  - https://docs.cypress.io/api/commands/contains
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Querying elements (get, find, contains, data-cy)

## Commands
```js
cy.get('[data-cy=submit]')                    // from document root, always
cy.get('form').find('input[name=email]')     // scoped to previous subject
cy.contains('Sign in')                         // deepest element containing text
cy.contains('button', 'Sign in')               // selector + text: preferred
cy.contains('[data-cy=row]', /order #10\d\d/) // regex
cy.get('li').eq(2); cy.get('li').first(); cy.get('li').filter('.active');
cy.get('table').within(() => { cy.get('tr').should('have.length', 5) });
```
`cy.get` inside a chain still searches from the root (or the `within` scope), unlike `.find`.

## Selector priority (Cypress best practices)
1. `data-cy` / `data-test` / `data-testid` attributes: isolated from CSS/JS changes.
2. `cy.contains` for text the user sees, when text change should fail the test.
3. Avoid: tag, class, id styling hooks, `nth-child`.
The element selector in `cypress open` proposes `data-cy` selectors first. The API is `Cypress.ElementSelector.defaults({ selectorPriority: [...] })` (renamed from `Cypress.SelectorPlayground` in Cypress 15.0.0). Default priority on 16.2.0: `data-cy`, `data-test`, `data-testid`, `data-qa`, `name`, `id`, `class`, `tag`, `attributes`, `nth-child`.

## Retry semantics
Queries (`get`, `find`, `contains`, `eq`, `filter`) retry until the assertion attached passes or `defaultCommandTimeout` (4s) expires. Only the **last query chain** before an assertion retries; actions break the chain.

## Gotchas
- `cy.contains` matches substrings and normalises whitespace; with `{ matchCase: false }` it is case-insensitive.
- `cy.get('button').contains('Save')` yields the button containing Save, not all buttons.
- Querying a selector that matches many then calling `.click()` fails unless `{ multiple: true }`.

## Verify
Run on Cypress 16.2.0: `get`/`find`/`contains` (incl. regex and whitespace normalisation: `cy.contains('a b')` matched `<p>  a   b </p>`), `eq`/`first`/`filter`, `within` with `cy.root()` and `withinSubject: null`, `matchCase: false`, and the multi-element click error. The element selector suggests the same selectors used in the spec; tests survive a CSS class rename.
