---
id: computing-software.qa-testing-engineering.playwright.test-id-attribute-config
name: test-id-attribute-config
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [testidattribute, getbytestid, data-testid-playwright, playwright-config, data-testid, locator-strategy]
level: practitioner
status: verified
description: "Use getByTestId in Playwright and configure testIdAttribute (data-qa, data-cy) per project so tests share an app's existing test-id convention."
sources:
  - https://playwright.dev/docs/locators#locate-by-test-id
  - https://playwright.dev/docs/api/class-selectors#selectors-set-test-id-attribute
  - https://playwright.dev/docs/test-use-options
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Configuring testIdAttribute and getByTestId

**Goal:** stable hooks for elements with no good accessible name, using whatever attribute the app already ships.

## Default
`page.getByTestId('submit')` matches `data-testid="submit"` (exact, case-sensitive string match; run here: `data-testid="Row"` matched `getByTestId('Row')` but not `'row'` or `'Ro'`).

## Change the attribute
```ts
// playwright.config.ts
export default defineConfig({
  use: { testIdAttribute: 'data-qa' },
});
```
Per project (e.g. legacy app uses `data-cy`):
```ts
projects: [
  { name: 'legacy', use: { testIdAttribute: 'data-cy', baseURL: 'https://legacy.test' } },
]
```
Library mode / Python:
```ts
import { selectors } from '@playwright/test';
selectors.setTestIdAttribute('data-qa');
```
```python
playwright.selectors.set_test_id_attribute("data-qa")
```

## Conventions that age well
- Name by purpose, not position: `cart-checkout`, not `button-3`.
- Put ids on containers for lists, then use role inside: `page.getByTestId('order-row').filter({ hasText: '#1042' }).getByRole('button', { name: 'Refund' })`.
- Keep test ids in production builds unless there is a size/privacy reason; stripping them (babel-plugin-react-remove-properties) means tests must run against a non-prod build.

## Gotchas
- Call `setTestIdAttribute` before creating pages; set in config to avoid ordering issues.
- `getByTestId` takes a string or regex; regex `/^row-/` is handy for generated ids (run here, it matched `data-testid="row-1"`).
- Run here with projects `chromium` (`data-qa`) and `legacy` (`data-cy`): the same page gave `getByTestId('x')` text `a` and `c` respectively, so per-project `use.testIdAttribute` works.
- Test ids do not prove accessibility; pair with role-based assertions on key flows.

## Verify
`npx playwright test --list` runs; a quick `await expect(page.getByTestId('x')).toBeVisible()` passes on the configured attribute.
