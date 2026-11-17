---
id: computing-software.qa-testing-engineering.playwright.playwright-input-actions
name: playwright-input-actions
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-actions, setinputfiles, fill, selectoption, dragto, keyboard-press]
level: practitioner
status: docs-checked
description: "Perform Playwright input actions correctly: fill vs pressSequentially, check, selectOption, setInputFiles for uploads, dragTo, hover, focus and keyboard shortcuts."
sources:
  - https://playwright.dev/docs/input
  - https://playwright.dev/docs/api/class-locator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input actions

**Goal:** drive form controls the way the app expects, without flaky key-by-key hacks.

## Text
```ts
await page.getByLabel('Name').fill('Ada');          // focuses, fills, triggers an input event
await page.getByLabel('Name').clear();
await page.getByLabel('Search').pressSequentially('pla', { delay: 50 }); // only if the page has special keyboard handling
await page.getByLabel('Search').press('Enter');
await page.keyboard.press('ControlOrMeta+A');       // Control on Windows/Linux, Meta on macOS
```

## Checkboxes, radios, selects
```ts
await page.getByRole('checkbox', { name: 'Agree' }).check();   // throws if not checked afterwards
await page.getByRole('radio', { name: 'Express' }).check();
await page.getByLabel('Country').selectOption('NZ');            // by value or label
await page.getByLabel('Tags').selectOption(['a', 'b']);         // multi-select
await page.getByLabel('Country').selectOption({ label: 'New Zealand' });
```
`selectOption` works on `<select>` elements; for custom dropdowns click to open and then click the option by role.

## Files
```ts
await page.getByLabel('Upload').setInputFiles('fixtures/a.pdf');
await page.getByLabel('Upload').setInputFiles(['a.png', 'b.png']);
await page.getByLabel('Upload').setInputFiles([]);              // clear
await page.getByLabel('Upload').setInputFiles({ name: 'x.txt', mimeType: 'text/plain', buffer: Buffer.from('hi') });
// No <input> visible (button opens picker):
const chooser = page.waitForEvent('filechooser');
await page.getByRole('button', { name: 'Attach' }).click();
await (await chooser).setFiles('a.pdf');
```

## Mouse
```ts
await page.getByText('Item 1').dragTo(page.getByText('Bin'));
await page.getByRole('img').hover();
await page.getByRole('row').first().dblclick();
await page.getByText('menu').click({ button: 'right', modifiers: ['Shift'] });
```
For precise control use `hover()`, `mouse.down()`, `hover()` on the target and `mouse.up()`. If the page relies on `dragover`, at least two mouse moves are needed, so repeat the target `hover()` or `mouse.move()`.

## Gotchas
- `fill` triggers an `input` event, while `pressSequentially` sends `keydown`, `keypress`/`input` and `keyup` for each character; use it only when the page has special keyboard handling.
- `check()` throws if the element is not a checkbox or radio, or is not checked after the click; that is a real bug signal.
- Relative `setInputFiles` paths resolve against the current working directory, not the spec file; the docs use `path.join(__dirname, ...)`.

## Verify
Assert the resulting state, not just that the action ran: `toHaveValue`, `toBeChecked`, `toHaveValues`, uploaded file name visible.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: fill, clear, pressSequentially and press behaviour, ControlOrMeta, check() semantics, selectOption by value, label and array, setInputFiles with paths, an empty array, buffer payloads and relative-path resolution, the filechooser event, dragTo and manual drag steps including the two-mouse-move note for dragover, click options button and modifiers, hover and dblclick.

Method: documentation only; no commands were run.
