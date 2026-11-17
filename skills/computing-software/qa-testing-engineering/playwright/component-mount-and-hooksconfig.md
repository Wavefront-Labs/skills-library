---
id: computing-software.qa-testing-engineering.playwright.component-mount-and-hooksconfig
name: component-mount-and-hooksconfig
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [ct-mount, hooksconfig, playwright-ct, component-testing-playwright]
level: practitioner
status: docs-checked
description: "Mount React, Vue and Svelte components in Playwright component tests with providers via hooksConfig, beforeMount/afterMount, props, events and update/unmount."
sources:
  - https://playwright.dev/docs/test-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mounting components with stories (replacing hooksConfig)

**Goal:** render a component in a real browser with the app's providers (router, theme, store) and assert behaviour, using Playwright's current framework-agnostic component testing.

## Status of the old API
The experimental `@playwright/experimental-ct-react`, `-ct-react17` and `-ct-vue` packages (with `hooksConfig`, `beforeMount`, `afterMount`, the `router` fixture and `ctViteConfig`) have been removed and are no longer published. Projects still on them should stay on Playwright 1.62 until migrated.

## Current pattern: story plus gallery
- A story is a small wrapper component that embeds the component under test in one scenario: hard-coded props, mock data, providers, recorded callbacks. Each named export is one scenario.
- The gallery is a single page under `playwright/gallery/`, served by your own dev server, that exposes `window.mount(params)` and `window.unmount()` and renders a story into `#root`. The docs suggest asking a coding agent to implement it for your framework.
- Tests import `test` and `expect` from plain `@playwright/test` and use the built-in `mount` fixture.

```ts
// playwright.config.ts
projects: [{
  name: 'components',
  testDir: './tests/components',
  use: {
    ...devices['Desktop Chrome'],
    baseURL: 'http://localhost:5173/playwright/gallery/index.html',
    serviceWorkers: 'block',
    reuseContext: true,
  },
}],
webServer: { command: 'npm run dev', url: 'http://localhost:5173/playwright/gallery/index.html', reuseExistingServer: !process.env.CI },
```
`mount` navigates to `baseURL`, so it must point at the gallery. `serviceWorkers: 'block'` stops the app's service worker shadowing `page.route()` mocks; `reuseContext: true` reuses the browser context between tests in a worker.

```tsx
// src/components/Button.story.tsx
export const Primary = () => <Button title='Submit' />;
export const WithTitle = ({ title = 'Default' }: { title?: string }) => <Button title={title} />;

// tests/components/button.spec.ts
import { test, expect } from '@playwright/test';
test('renders primary button', async ({ mount }) => {
  const component = await mount('components/Button/Primary');
  await expect(component.getByRole('button')).toHaveText('Submit');
});
const c = await mount<typeof WithTitle>('Button/WithTitle', { title: 'Hello' });
await c.update({ title: 'Changed' });   // re-renders the same story without remounting
```

## Migration map
| Old | New |
|---|---|
| `hooksConfig` per-test variation | plain serialisable props passed to `mount`, interpreted by the story |
| `beforeMount` / `afterMount` | body of the gallery's `window.mount` (global) or story decorators (per story) |
| `router` fixture / MSW in Node | `page.route()` in the test (register before `mount()`), or MSW `setupWorker` inside a story |
| callbacks passed from the test | the story owns state and callbacks and records effects into `data-testid` inputs; assert with `toHaveValue()` |
| `ctViteConfig`, `ctPort`, `ctTemplateDir` | gone; the gallery runs through your own dev server (`webServer` and `baseURL`) |

## Gotchas
- Keep props to plain serialisable values; live objects and callbacks cannot cross from Node to the browser.
- Do not reach into component internals or instances from test code; observe and interact like a user.

## Verify
`mount('components/Button/Primary')` renders and the assertion passes; a story given a dark-theme prop shows the dark theme.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: that the @playwright/experimental-ct-react, -ct-react17 and -ct-vue packages have been removed and are no longer published (stay on Playwright 1.62 until migrated), the story and gallery pattern, the components project settings (baseURL, serviceWorkers block, reuseContext), the mount fixture and update() semantics, serialisable-only props, page.route before mount, and the migration table from hooksConfig, beforeMount and the router fixture.

Method: documentation only; no commands were run.
