---
id: computing-software.web-development.web-accessibility.inspecting-the-accessibility-tree
name: inspecting-the-accessibility-tree
category: computing-software
field: web-development
product: web-accessibility
tags: [accessibility-tree, accessible-name-computation, aria-snapshot, devtools-accessibility, accessibility-insights, accessibility-testing]
level: practitioner
status: verified
description: "Inspecting what assistive tech receives: DevTools accessibility panes, accessible name computation order, ignored nodes, Playwright ARIA snapshots and OS-level inspectors."
sources:
  - https://developer.chrome.com/docs/devtools/accessibility/reference
  - https://www.w3.org/TR/accname-1.2/
  - https://playwright.dev/docs/aria-snapshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting the accessibility tree

Screen readers do not read your DOM; they read the accessibility tree the browser builds from it (roles, names, states, relationships).

## 1. Browser tools
- **Chrome/Edge**: Elements > Accessibility pane shows the computed role, name (and which source supplied it), description, states, and the ancestor tree. Enable "full-page accessibility tree" to toggle the Elements panel into tree view.
- **Firefox**: Accessibility Inspector: tree view, checks for contrast/keyboard/labels, "Show Tabbing Order", simulate colour deficiencies.
- **Safari**: Elements > Node > Accessibility section.
- OS level: macOS Accessibility Inspector (Xcode), Windows Accessibility Insights for Windows / Inspect.exe (UI Automation tree), for native webviews and Electron.

## 2. Name computation order (simplified accname)
1. `aria-labelledby` (concatenates referenced elements' text, even hidden ones)
2. `aria-label`
3. Native labelling: `<label for>`, `alt`, `<caption>`, `<legend>`, `<figcaption>`, `title` on `<abbr>` etc.
4. Content (only for roles that allow name from content: buttons, links, headings, options, cells...)
5. `title`, then `placeholder` as last resorts (unreliable)
Common surprises: `aria-label` on a `div`/`span` without a role is prohibited by ARIA 1.2 and support varies (Chromium's tree still exposed the name, run); `aria-labelledby` overrides a visible `<label>`; icon-only buttons with an `<svg>` and no text have no name.

## 3. Ignored and hidden nodes
`display:none`, `visibility:hidden`, `hidden`, `aria-hidden="true"` and `inert` remove nodes from the tree; `role="presentation"`/`none` strips semantics but keeps content. Check that decorative wrappers are not exposed as noisy groups and that real content is not accidentally hidden.

## 4. Automate snapshots
```ts
await expect(page.getByRole("navigation", { name: "Main" })).toMatchAriaSnapshot(`
  - navigation "Main":
    - list:
      - listitem:
        - link "Home"
      - listitem:
        - link "Pricing"
`);
```
Playwright ARIA snapshots (the example above passed on Playwright 1.64.1; link entries also record `/url`) lock down roles/names so refactors cannot silently break semantics. Prefer `getByRole` locators in all tests: if the test cannot find it by role and name, neither can a screen reader user.

## Verify
- [ ] Every interactive element on the page has a role and a non-empty, meaningful accessible name in the Accessibility pane.
