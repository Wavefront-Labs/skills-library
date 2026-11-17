---
id: computing-software.qa-testing-engineering.playwright.actionability-and-auto-waiting
name: actionability-and-auto-waiting
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [actionability, auto-waiting-checks, force-click, trial-run, playwright-actions]
level: practitioner
status: verified
description: "Know Playwright's actionability checks (visible, stable, enabled, receives events, editable), fix 'intercepts pointer events' errors, and use force and trial correctly."
sources:
  - https://playwright.dev/docs/actionability
  - https://playwright.dev/docs/api/class-locator#locator-click
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-waiting and actionability checks

**Goal:** know what Playwright waits for before each action, so failures point at real UI problems.

## Checks per action (docs table)
| Action | Visible | Stable | Receives events | Enabled | Editable | Not inert |
|---|---|---|---|---|---|---|
| click, dblclick, check, uncheck, setChecked, tap | yes | yes | yes | yes | - | yes |
| hover, dragTo | yes | yes | yes | - | - | - |
| fill, clear | yes | - | - | yes | yes | yes |
| selectOption | yes | - | - | yes | - | - |
| selectText | yes | - | - | - | - | - |
| screenshot | yes | yes | - | - | - | - |
| scrollIntoViewIfNeeded | - | yes | - | - | - | - |
| press, pressSequentially, focus, blur, dispatchEvent, setInputFiles | - | - | - | - | - | - |

- **Visible:** non-empty bounding box and not `visibility:hidden`. `display:none` and zero-size elements are not visible; `opacity:0` elements are.
- **Stable:** same bounding box for at least two consecutive animation frames (animations finished).
- **Enabled:** not `disabled` (also inside a disabled `<fieldset>`, or under `aria-disabled=true`). **Editable:** enabled and not readonly. **Not inert:** not under an `inert` attribute and not outside an open modal `<dialog>`.
- **Receives events:** the element is the hit target at the action point, not covered by an overlay.
- Playwright retries until checks pass or the action timeout expires (`actionTimeout`, default none, so the test timeout bounds it; run here: `locator.click: Test timeout of 3000ms exceeded.` with no action timeout, `TimeoutError: locator.click: Timeout 700ms exceeded.` with `{ timeout: 700 }`).

## Reading failures
```
locator.click: Timeout 5000ms exceeded.
  - element is visible, enabled and stable
  - <div class="cookie-banner"> intercepts pointer events
```
Fix the cause: dismiss the banner (or `page.addLocatorHandler` for overlays that appear at random), wait for the spinner to disappear with `await expect(spinner).toBeHidden()`.

## force and trial
```ts
await btn.click({ force: true });   // skips the non-essential checks (docs: e.g. receives-events). Hides real bugs; avoid.
await btn.click({ trial: true });   // runs checks but does not click: probe "is it clickable now?"
```
Run here (Playwright 1.64): `force` on a button covered by an overlay dispatched the click at the point, so it hit the overlay, not the button; `force` on a `disabled` button raised no error (enabled check skipped); `force` on a `display:none` button still failed with `Element is not visible`. So visibility is still required. Legit `force` uses: custom checkbox where the real `<input>` is visually hidden behind a styled label (better: click the label).

## addLocatorHandler for random overlays
```ts
await page.addLocatorHandler(page.getByRole('dialog', { name: 'Newsletter' }), async (d) => {
  await d.getByRole('button', { name: 'No thanks' }).click();
});
```

## Gotchas
- Actionability is not app readiness: a button can be enabled before its click handler is attached (hydration). Wait for a readiness signal (e.g. `await expect(page.locator('html[data-hydrated]')).toBeAttached()`).
- `isVisible()` / `isEnabled()` do not wait; use web-first assertions instead.

## Verify
Zero `force: true` without a justifying comment; overlay failures resolved by handling the overlay.
