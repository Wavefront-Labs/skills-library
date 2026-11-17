---
id: computing-software.qa-testing-engineering.playwright.locator-filtering-and-chaining
name: locator-filtering-and-chaining
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [locator-filter, locator-chaining, playwright-locators, getbyrole, has-text]
level: practitioner
status: verified
description: "Narrow Playwright locators with filter (hasText, has, hasNot, visible), chaining, and(), or(), and scoping inside list items instead of brittle CSS or XPath."
sources:
  - https://playwright.dev/docs/locators#filtering-locators
  - https://playwright.dev/docs/api/class-locator#locator-filter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering and chaining locators (Playwright)

**Goal:** precise, readable locators built from user-facing attributes, scoped step by step.

## Chaining (scope inside a parent)
```ts
const dialog = page.getByRole('dialog', { name: 'Edit address' });
await dialog.getByRole('textbox', { name: 'Postcode' }).fill('SW1A 1AA');
await dialog.getByRole('button', { name: 'Save' }).click();
```

## filter()
```ts
const row = page.getByRole('row').filter({ hasText: 'Order #1042' });
await row.getByRole('button', { name: 'Refund' }).click();

page.getByRole('listitem').filter({ hasText: /coffee/i });
page.getByRole('listitem').filter({ hasNotText: 'Out of stock' });
page.getByRole('listitem').filter({ has: page.getByRole('heading', { name: 'Beans' }) });
page.getByRole('listitem').filter({ hasNot: page.getByText('Sold out') });
page.getByRole('button').filter({ visible: true });      // newer releases (works on 1.64; `visible: false` matches invisible ones)
```
The inner `has` locator is relative to each candidate and must not start from outside it.

## Options on the locator call
`page.locator('article', { hasText: 'Beans', has: page.getByRole('img') })` is equivalent to filter.

## Combine
```ts
const submit = page.getByRole('button').and(page.getByTitle('Subscribe'));   // both must match
const okOrDismiss = page.getByRole('button', { name: 'OK' }).or(page.getByRole('button', { name: 'Dismiss' }));
await expect(okOrDismiss.first()).toBeVisible();
```
`or()` can match both; acting on it then throws a strict mode violation (run here: `resolved to 2 elements`), so take `.first()` or assert count if that is possible. In Python the methods are `or_()` and `and_()`.

## Patterns
- Table cell by row and column: filter row by text, then `getByRole('cell').nth(colIndex)` from the header index. `nth()` and `first()` are resolved inside each matched parent, so on the unfiltered rows `getByRole('cell').nth(2)` picks the third cell of every row.
- Repeated cards: `page.getByTestId('product-card').filter({ hasText: 'Beans' })`.

## Gotchas
- `hasText` is a substring match, case-insensitive for strings; use a regex anchored `^...$` for exact.
- Filtering on text that changes with locale breaks i18n runs; prefer test ids for non-semantic scoping.

## Verify
Locators resolve to exactly one element (no strictness errors), and the test survives DOM restructuring that keeps roles and names.
