---
id: computing-software.qa-testing-engineering.playwright.aria-snapshot-assertions
name: aria-snapshot-assertions
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [aria-snapshot, accessibility-tree, playwright-assertions, tomatcharia-snapshot, structural-testing]
level: practitioner
status: verified
description: "Assert page structure with Playwright ARIA snapshots: toMatchAriaSnapshot YAML templates, partial and regex matching, snapshot files, and updating them safely."
sources:
  - https://playwright.dev/docs/aria-snapshots
  - https://playwright.dev/docs/api/class-locatorassertions#locator-assertions-to-match-aria-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARIA snapshot assertions (Playwright)

**Goal:** assert what assistive technology sees (roles, names, structure) instead of DOM details or pixels. Available from Playwright 1.49.

## Inline template
```ts
await expect(page.getByRole('navigation', { name: 'Main' })).toMatchAriaSnapshot(`
  - navigation "Main":
    - link "Home"
    - link "Orders"
    - link /Basket \\(\\d+\\)/
`);
```
- YAML-like tree: `- role "accessible name"`, children indented, attributes like `[checked]`, `[level=2]`, `[expanded=false]`, text nodes as `- text: ...`.
- **Partial matching**: only listed nodes/attributes are checked; omitted siblings are allowed by default (run here: a template listing 2 of 3 links passed, and omitting the first link also passed). Use `- /children: equal` to require exact children (run here: the same partial template then failed); `- /children: contain` is also accepted. The generated snapshot adds `- /url: "..."` under links, which a template may omit.
- Regex names: `/Basket \(\d+\)/`.

## Generate the template
- `npx playwright codegen` -> "Assert snapshot" tool.
- `await locator.ariaSnapshot()` returns the current tree as a string (print and paste).
- Passing an empty string, `toMatchAriaSnapshot('')`, generates the snapshot; `--update-snapshots` (`-u`, mode `changed`) updates ones that no longer match. Without `-u` a run that generates a missing snapshot fails on purpose (run here: `A snapshot doesn't exist at ..., writing actual.`).

## Snapshot files
```ts
await expect(page.getByRole('main')).toMatchAriaSnapshot({ name: 'checkout-main.aria.yml' });
```
Stored next to the test in `<spec file>-snapshots/` (run here: `a.spec.ts-snapshots/nav.aria.yml`), customizable with `snapshotPathTemplate`; update with `npx playwright test --update-snapshots`. For inline templates `--update-source-method` is `patch` (default, writes a patch file for `git apply`), `3way` or `overwrite`.

## Use cases
- Navigation, forms and dialogs keep their accessible structure.
- Replace brittle text/structure assertions across many elements with one tree.
- Regression guard for component library upgrades.

## Gotchas
- Dynamic content (dates, counts) needs regex or omission.
- It checks the accessibility tree, not WCAG conformance; pair with axe scans.
- Over-specified snapshots (whole page) churn; snapshot the region you care about.

## Verify
Removing a label or changing a heading level fails the assertion, and updated snapshots are reviewed in the PR diff.
