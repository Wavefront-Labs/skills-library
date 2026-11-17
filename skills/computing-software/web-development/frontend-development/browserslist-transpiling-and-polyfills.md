---
id: computing-software.web-development.frontend-development.browserslist-transpiling-and-polyfills
name: browserslist-transpiling-and-polyfills
category: computing-software
field: web-development
product: frontend-development
tags: [build-tooling, browserslist, polyfills, babel, core-js, transpiling]
level: practitioner
status: verified
description: "Choosing browser targets with Browserslist, transpiling syntax with esbuild/SWC/Babel, adding only needed core-js polyfills, and avoiding over- or under-transpiling."
sources:
  - https://github.com/browserslist/browserslist
  - https://babeljs.io/docs/babel-preset-env
  - https://github.com/zloirock/core-js
  - https://web-platform-dx.github.io/web-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browserslist, transpiling and polyfills

## 1. Define targets from data
```
# .browserslistrc
> 0.5% and last 2 versions, not dead, Firefox ESR
# or Baseline-based (supported by browserslist 4.29; resolves to browser versions that support all Widely available features, i.e. interoperable for 30+ months):
baseline widely available
```
Check what it resolves to: `npx browserslist`. Update the caniuse database regularly: `npx update-browserslist-db@latest`. Base targets on your own analytics, not global stats.

## 2. Syntax vs APIs
- **Syntax** (optional chaining, class fields) is transpiled by the compiler: Babel `preset-env`, SWC `env.targets`, esbuild `target: ["es2020","safari14"]`, Vite `build.target` (default `"baseline-widely-available"`, a date-fixed set per Vite major).
- **APIs** (`Array.prototype.toSorted`, `structuredClone`, `Promise.withResolvers`) need polyfills; transpilers do not add them.
- Babel `useBuiltIns: "usage", corejs: "3.51"` injects only polyfills used and missing in targets. Vite: `@vitejs/plugin-legacy` builds a separate legacy bundle with `nomodule`.

## 3. Pitfalls
- Over-transpiling to ES5 doubles bundle size and slows modern browsers. Modern-only targets are fine for most apps in 2026.
- **node_modules are usually not transpiled** - a dependency shipping ES2022 breaks old Safari even if your code is transpiled. Check with `npx es-check es2020 "dist/**/*.js"` (add `--module` for ESM output, otherwise `export` is a syntax error). It checks syntax only: a file using `[1].at(0)` passes `es2020`, so APIs still need a polyfill review.
- Polyfill services that sniff user agents (old polyfill.io domain was compromised in 2024) - never load third-party polyfill CDNs; bundle core-js yourself.
- Polyfills cannot fix missing CSS features or engine behaviour (e.g. `:has()`, container queries) - use `@supports` and progressive enhancement.
- TypeScript `target` only affects syntax; `lib` only affects types - neither polyfills.

## 4. CSS
Autoprefixer and Lightning CSS read the same Browserslist config for vendor prefixes and syntax lowering (nesting, `oklch` fallbacks).

## Verify
`es-check` on the output; test the oldest target browser on BrowserStack/real device; bundle analyzer shows polyfill weight.
