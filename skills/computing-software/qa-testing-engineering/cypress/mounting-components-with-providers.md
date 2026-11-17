---
id: computing-software.qa-testing-engineering.cypress.mounting-components-with-providers
name: mounting-components-with-providers
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-mount, cypress-component-testing, component-testing, react, vue, test-providers]
level: practitioner
status: verified
description: "Mount components in Cypress component testing with providers (router, store, theme, i18n, query client), custom mount commands, props, stubs and spies."
sources:
  - https://docs.cypress.io/app/component-testing/react/overview
  - https://docs.cypress.io/app/component-testing/vue/overview
  - https://docs.cypress.io/app/component-testing/get-started
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mounting components with providers and stubs (Cypress CT)

## Custom mount with providers (React)
```tsx
// cypress/support/component.tsx
import { mount, MountOptions } from 'cypress/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '../../src/theme';

Cypress.Commands.add('mount', (component: React.ReactNode, { route = '/', ...options } = {}) => {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return mount(
    <QueryClientProvider client={qc}>
      <ThemeProvider><MemoryRouter initialEntries={[route]}>{component}</MemoryRouter></ThemeProvider>
    </QueryClientProvider>, options);
});
```
Declare the type on `Cypress.Chainable` (see typing-custom-commands-typescript).

## Test with props, spies and stubs
```tsx
it('submits the form', () => {
  const onSubmit = cy.spy().as('onSubmit');
  cy.mount(<AddressForm onSubmit={onSubmit} initial={{ postcode: '' }} />);
  cy.get('[name=postcode]').type('SW1A 1AA');
  cy.contains('button', 'Save').click();
  cy.get('@onSubmit').should('have.been.calledOnceWith', Cypress.sinon.match({ postcode: 'SW1A 1AA' }));
});
```
- Network: `cy.intercept` works in CT for components that fetch.
- Module stubs: prefer dependency injection via props/context.

## Vue
Register once in `cypress/support/component.js`: `import { mount } from 'cypress/vue'; Cypress.Commands.add('mount', mount);`
```js
cy.mount(Counter, { props: { start: 2 }, global: { plugins: [createTestingPinia({ createSpy: cy.spy }), router] } });
```

## Config
```js
component: { devServer: { framework: 'react', bundler: 'vite' }, specPattern: 'src/**/*.cy.{ts,tsx}' }
```
With Vite the project needs a `vite.config.*` (with the framework plugin, e.g. `@vitejs/plugin-react`) discoverable upwards, or pass `viteConfig` in `devServer`; without one the run stops with "a configuration file was not found". Cypress 16 requires Vite 8+ for component testing (changelog 16.0.0). The test project used `cypress/support/component-index.html` containing `<div data-cy-root></div>`.
Global CSS: import in `cypress/support/component.ts`. Viewport via `cy.viewport` or config.

## Gotchas
- Providers missing -> components crash with context errors; centralise them in the custom mount.
- Real query client retries make error states slow; disable retries in tests.

## Verify
Run on Cypress 16.2.0 (React 19.3, Vite 8.3, Vue 3.5, Pinia 4, vue-router 5): the React custom `mount` with `QueryClientProvider`, `ThemeProvider` and `MemoryRouter` plus `cy.spy` and `have.been.calledOnceWith(Cypress.sinon.match(...))`, the `cy.intercept` delay example, and the Vue `createTestingPinia` + router mount all passed. Components mount with one call, interactions assert on spies and DOM, and CT runs in CI with `cypress run --component`.
