---
id: computing-software.qa-testing-engineering.playwright.locator-strictness-and-nth
name: locator-strictness-and-nth
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [locator-strictness, playwright-locators, nth, first, strict-mode-violation]
level: practitioner
status: verified
description: "Handle Playwright strict mode: why actions on multi-match locators throw, how to read the error, and when first(), last() and nth() are acceptable versus better scoping."
sources:
  - https://playwright.dev/docs/locators#strictness
  - https://playwright.dev/docs/api/class-locator#locator-nth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strictness violations and nth/first

**Goal:** every action targets the one element you mean; resolve ambiguity deliberately.

## The rule
Actions (`click`, `fill`, `check`...) and most assertions on a locator require it to resolve to exactly one element. Otherwise:
```
Error: strict mode violation: getByRole('button', { name: 'Delete' }) resolved to 3 elements:
    1) <button ...>Delete</button> aka getByTestId('row-1').getByRole('button', { name: 'Delete' })
    2) ...
```
The error suggests a unique locator for each match (run here, it was a chain such as `getByRole('listitem').filter({ hasText: 'Filters Delete' }).getByRole('button')`): use them as hints for scoping. `textContent()` and `toHaveText('a')` on a multi-match locator throw the same error.

## Fix order of preference
1. **Scope** to a container: `page.getByRole('row').filter({ hasText: 'Alice' }).getByRole('button', { name: 'Delete' })`.
2. **More specific name**: `{ name: 'Delete Alice', exact: true }` (fix accessible names in the app if ambiguous to users too).
3. **Test id** on the specific element.
4. **Position** only when position is the requirement: `first()`, `last()`, `nth(i)` (0-based).

## Multi-element operations (not strict)
```ts
await expect(page.getByRole('listitem')).toHaveCount(3);
await expect(page.getByRole('listitem')).toHaveText(['Beans', 'Filters', 'Mug']);
const names = await page.getByRole('listitem').allInnerTexts();
for (const row of await page.getByRole('row').all()) { /* each is a strict locator */ }
```
`count()`, `all()`, `allTextContents()` work on many elements.

## Python
`page.get_by_role("row").nth(2)`, `.first`, `.last` (properties in Python, per the docs' `or_(dialog).first` example).

## Gotchas
- `first()` silences the error and silently picks a different element when the DOM order changes.
- `all()` does not wait for elements; assert the count first if the list loads asynchronously (run here: `all()` and `count()` returned 0 right after a script inserted the items 400 ms later; `toHaveCount(2)` waited).

## Verify
No `first()`/`nth()` without a comment explaining why position matters, and strictness errors are fixed by scoping.
