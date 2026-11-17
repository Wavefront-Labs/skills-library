---
id: computing-software.web-development.web-performance.replacing-heavy-dependencies
name: replacing-heavy-dependencies
category: computing-software
field: web-development
product: web-performance
tags: [dependency-diet, bundle-size, tree-shaking, native-apis, javascript-performance]
level: practitioner
status: docs-checked
description: "Cutting JavaScript by replacing heavy dependencies: finding culprits, native replacements for moment, lodash, axios and jQuery, and guarding with budgets."
sources:
  - https://eslint.org/docs/latest/rules/no-restricted-imports
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports
  - https://github.com/es-tooling/module-replacements
  - https://youmightnotneed.com/lodash
  - https://web.dev/articles/reduce-javascript-payloads-with-tree-shaking
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Replacing heavy dependencies

## 1. Find the weight
- `webpack-bundle-analyzer`, `rollup-plugin-visualizer` or `source-map-explorer` show which packages dominate a bundle.
- Check a candidate's size and tree-shakeability before adding it (a package-size site, or `size-limit` in your repo).
- `npx knip` finds unused dependencies and exports.

## 2. Common swaps
| Heavy | Replace with |
|---|---|
| moment | `Intl.RelativeTimeFormat` for relative times; see the e18e `module-replacements` list for others |
| lodash (full import) | native (`structuredClone`, `Object.groupBy`, `Array.prototype.findLast`, `Array.prototype.toSorted`), or per-method `lodash-es` imports |
| axios | `fetch` with `AbortSignal.timeout` for timeouts |
| jQuery | native DOM APIs and `fetch` |
| uuid | `crypto.randomUUID()` |
| classnames | `clsx` |
| numeral / accounting.js | `Intl.NumberFormat` |
| Full icon packs | per-icon imports or an SVG sprite |
| Chart library for one sparkline | inline SVG path |
| Polyfill-heavy packages | the e18e `module-replacements` list for native alternatives |

## 3. Import hygiene
- Tree-shaking works on ES module imports and relies on the package's `sideEffects` setting (web.dev). Prefer named imports from an ESM build such as `lodash-es`.
- Next.js `optimizePackageImports` optimises barrel imports for the packages it lists (for example `lodash-es`).
- Load rarely used heavy features on demand: `const { default: Editor } = await import("./editor")` on click.

## 4. Keep it from coming back
- Size budgets in CI (for example `size-limit`) fail PRs that add weight.
- Review new dependencies in PRs: size, maintenance, transitive deps, licence.
- ESLint `no-restricted-imports` to ban `moment`, full `lodash`, etc.

## Verify
- [ ] Bundle analyser before/after shows reduced main-chunk size; budgets enforced in CI; replaced functionality covered by tests (especially dates and number formatting).

## Checked
2026-10-28 Confirmed on MDN, the Next.js, ESLint, size-limit, source-map-explorer, webpack-bundle-analyzer, rollup-plugin-visualizer, Knip, clsx and web.dev pages: `structuredClone`, `Object.groupBy`, `Array.prototype.findLast`/`toSorted`, `AbortSignal.timeout`, `crypto.randomUUID()`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat`, `optimizePackageImports` (lists `lodash-es`), `no-restricted-imports`, `size-limit`, `clsx`, `sideEffects` and tree-shaking, the e18e module-replacements list. Removed (not on the fetched pages): `vite-bundle-visualizer`, `@next/bundle-analyzer`, bundlephobia and pkg-size (the bundlephobia page returned a stub), Temporal, date-fns/dayjs, `bundlesize`, Lighthouse CI, the `lodash` default-import claim and the 20-line wrapper wording.
Method: documentation only; no commands were run.
