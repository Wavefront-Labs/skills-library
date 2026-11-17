---
id: computing-software.qa-testing-engineering.playwright.user-facing-locator-priority
name: user-facing-locator-priority
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [user-facing-locators, getbyrole, getbylabel, getbytext, playwright-locators, accessible-name]
level: practitioner
status: verified
description: "Pick Playwright locators in the documented priority order (role, label, placeholder, text, alt, title, test id) and fix the app when a good locator cannot be written."
sources:
  - https://playwright.dev/docs/locators
  - https://playwright.dev/docs/best-practices#use-locators
  - https://www.w3.org/TR/accname-1.2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role, label, placeholder and text locator priority

**Goal:** locators that read like the user's view of the page and survive markup refactors.

## Priority
The docs recommend prioritizing role locators and user-facing attributes, and list the built-ins as role, text, label, placeholder, alt text, title, test id; they do not publish a strict ranking. The order below is a practical one:
| Locator | Use for |
|---|---|
| `getByRole(role, { name })` | buttons, links, headings, checkboxes, rows, dialogs: almost everything |
| `getByLabel(text)` | form controls with a `<label>`, `aria-label` or `aria-labelledby` |
| `getByPlaceholder(text)` | inputs that only have a placeholder (flag as an a11y issue) |
| `getByText(text)` | non-interactive text (paragraphs, toasts) |
| `getByAltText` / `getByTitle` | images, elements with title |
| `getByTestId(id)` | when there is no stable user-facing handle |
| `locator(css/xpath)` | last resort |

```ts
await page.getByRole('button', { name: 'Sign in' }).click();
await page.getByLabel('Email').fill('a@b.test');
await expect(page.getByRole('heading', { level: 1 })).toHaveText('Dashboard');
await page.getByRole('checkbox', { name: 'Remember me' }).check();
await page.getByRole('link', { name: /privacy/i }).click();
```

## Name matching
- `name` is the **accessible name** (label text, aria-label, inner text, alt).
- Default is case-insensitive substring; `exact: true` for whole-string, case-sensitive; regex for patterns.
- Extra role options (from the 1.64 typings): `checked`, `pressed`, `expanded`, `selected`, `level`, `includeHidden`, `disabled`, `description`.

## When getByRole fails
1. Run `npx playwright codegen` or the Locator picker in UI mode; it proposes the best locator.
2. Inspect the accessibility tree in DevTools (Elements > Accessibility). A `<div onclick>` has no role: that is an app defect (keyboard and screen-reader users cannot use it either). File it; use a test id meanwhile.
3. Icon-only buttons need `aria-label`; ask for it instead of using CSS.

## Gotchas
- `getByText('Save')` also matches "Save draft"; prefer role+name or `exact: true`.
- Translations change names: run the suite in one locale or use test ids for i18n-heavy UIs.
- Hidden elements are excluded from `getByRole` unless `includeHidden: true` (run here: 3 visible list items, 4 with `includeHidden`).
- Run here: `getByRole('button', { name: 'Save' })` matched both "Save" and "Save draft"; with `exact: true` only "Save"; `getByText('Save', { exact: true })` likewise.

## Verify
Grep the suite for `page.locator(`; each remaining CSS/XPath locator should have a comment explaining why no user-facing locator works.
