---
id: computing-software.software-engineering.javascript.js-baseline-feature-adoption
name: js-baseline-feature-adoption
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, baseline-widely-available, js-versions]
level: practitioner
status: docs-checked
description: "Decide when to use new web platform features using Baseline: Newly and Widely available, the core browser set, yearly targets, and tooling that reads Baseline data."
sources:
  - https://web.dev/baseline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baseline status and adopting new features

- Baseline is defined by the WebDX Community Group (it originated with the Chrome team). It has two stages: "Newly available" (supported by all core browsers, so interoperable) and "Widely available" (30 months have passed since the newly interoperable date). Before that a feature has "Limited availability".
- Core browser set: Chrome (desktop and Android), Edge, Firefox (desktop and Android), Safari (macOS and iOS).
- Baseline targets: features that become Newly available in a year form a feature set, such as Baseline 2024 or Baseline 2025. Choose a target for your project and check features against it.
- Where to look up status: MDN, Can I Use, the WebStatus.dev dashboard.
- Tooling the page lists: a Lighthouse "Baseline features" audit, Baseline queries in Browserslist, the `web-features` npm package (data for building your own tools), Baseline support in VS Code, and ESLint support for enforcing Baseline CSS features.
- For polyfills the page links guides on choosing a Baseline target and on how to think about Baseline and polyfills; read them before deciding to ship a shim.
- Gate newer APIs with feature detection or a transpile or polyfill step, and review shims when your Baseline target moves.

Self-check: your support matrix lists the Baseline status of each newer API in use.

## Checked

Checked 2026-11-08 against the web.dev Baseline page (stages, 30 month rule, core browser set, targets, tooling list, lookup sites). Removed: the TC39 stage list, the Node LTS schedule pointer and the `eslint-plugin-baseline-js` package suggestion (not on the cited page).
Method: docs-only read of cited pages, 2026-11-08
