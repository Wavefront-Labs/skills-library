---
id: computing-software.qa-testing-engineering.test-automation.polyfill-and-browser-feature-support-testing
name: polyfill-and-browser-feature-support-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [polyfill-testing, browserslist, cross-browser-testing, progressive-enhancement, feature-detection]
level: practitioner
status: docs-checked
description: "Test browser feature support: derive targets from browserslist, lint unsupported APIs with eslint-plugin-compat, and test feature-detection fallbacks."
sources:
  - https://github.com/browserslist/browserslist
  - https://github.com/amilajack/eslint-plugin-compat
  - https://developer.mozilla.org/en-US/docs/Glossary/Polyfill
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser feature support and polyfill testing

**Goal:** every browser in the support policy gets working code, either native or via polyfills and fallbacks. A polyfill is code (usually JavaScript) that provides modern functionality on older browsers that lack it; native implementations are faster and can do more, so polyfills are not used exclusively (MDN).

## Know the targets
- Browserslist reads queries from `package.json` (`"browserslist"`) or a `.browserslistrc` file (one query per line, `#` comments). Run `npx browserslist` in the project directory to see which browsers the queries select; `npx browserslist '> 0.3%, not dead'` tests a query ad hoc.
- With no configuration, Browserslist uses its defaults: `> 0.5%, last 2 versions, Firefox ESR, not dead`. Its docs recommend `last 2 versions, not dead, > 0.2%` if you change the defaults.
- Queries such as `last 2 versions` use caniuse-lite data. `update-browserslist-db` is the CLI that refreshes that data; `browserslist-update-action` is a GitHub Action that runs it and proposes a pull request. Stale data silently changes which browsers a query selects.
- Browserslist supports several environments (for example `production` and `modern`) in one config. The QA browser matrix should match the targets your build tools read.

## Lint unsupported APIs
- `eslint-plugin-compat` checks the browser compatibility of your code against the browserslist targets. Flat config: `import compat from "eslint-plugin-compat"; export default [compat.configs["flat/recommended"]];`.
- Mark APIs you polyfill in the ESLint `settings.polyfills` list (for example `"Promise"`, `"fetch"`, `"Array.prototype.push"`; instance methods need `.prototype.`) so they are not reported.
- By default feature detection such as `if (fetch) { ... }` does not trigger a report; set `settings.ignoreConditionalChecks` to `true` to lint those too.
- It targets the `production` browserslist environment by default; change it with `settings.browserslistOpts.env`.
- Linting ES APIs (as opposed to Web APIs) is experimental and off by default; enable with `settings.lintAllEsApis`.

## Runtime tests
- Run smoke tests on the oldest supported version of each engine in your browserslist.
- Exercise the detection path: remove the feature in a script that runs before the app loads, then confirm the fallback works and the console stays clean.
- Watch the console on old browsers for errors about missing functions or undefined globals, the signature of a missing polyfill.

## Verify
The lint rule passes in CI for the current browserslist, and smoke tests on the oldest version of each targeted engine show no console errors.

## Checked
2026-11-09. Confirmed against the browserslist README (npx browserslist, .browserslistrc, defaults, recommended query, update-browserslist-db, browserslist-update-action), the eslint-plugin-compat README (flat config, polyfills setting, ignoreConditionalChecks, browserslistOpts.env, lintAllEsApis, production default) and the MDN Polyfill glossary page. Removed unconfirmed material: es-check command, core-js useBuiltIns behaviour, specific API examples (structuredClone, Array.prototype.at), Playwright/WebKit and BrowserStack advice, CSS fallback examples.
Method: documentation only; no commands were run.
