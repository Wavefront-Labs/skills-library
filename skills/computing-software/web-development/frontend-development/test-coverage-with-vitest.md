---
id: computing-software.web-development.frontend-development.test-coverage-with-vitest
name: test-coverage-with-vitest
category: computing-software
field: web-development
product: frontend-development
tags: [code-coverage, istanbul, vitest-coverage, coverage-thresholds, lcov, frontend-testing]
level: practitioner
status: verified
description: "Measuring test coverage in front-end projects: Vitest v8 vs istanbul providers, include/exclude, thresholds, ignore comments, CI reporting and E2E coverage."
sources:
  - https://vitest.dev/guide/coverage
  - https://vitest.dev/config/#coverage
  - https://playwright.dev/docs/api/class-coverage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test coverage with Vitest

## 1. Setup
```bash
npm i -D @vitest/coverage-v8        # or @vitest/coverage-istanbul
npx vitest run --coverage
```
```ts
// vitest.config.ts
export default defineConfig({ test: { coverage: {
  provider: "v8",
  include: ["src/**/*.{ts,tsx}"],                       // count untested files too
  exclude: ["src/**/*.stories.tsx", "src/**/*.d.ts", "src/mocks/**", "src/main.tsx"],
  reporter: ["text-summary", "html", "lcov"],
  thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 },
}}});
```
- **v8**: uses the engine's native coverage, fast, no instrumentation; Vitest remaps it to source with AST awareness so results are close to istanbul.
- **istanbul**: instruments code; works in any runtime; slightly slower; most precise branch data.
Set `include` explicitly, otherwise files no test imports are invisible and the percentage lies (a 1-line untested file in `include` showed as 0% in `lcov.info`).

## 2. Ignoring code honestly
`/* v8 ignore next */`, `/* v8 ignore start */ ... /* v8 ignore stop */`, or `/* istanbul ignore next */` for genuinely untestable branches (platform guards). The Vitest docs warn that esbuild strips non-legal comments from TypeScript and suggest `/* v8 ignore next -- @preserve */` (the hint may then reach production builds). In a test with Vitest 5.0.5 on Vite 8, plain `v8 ignore next` and `istanbul ignore next` in a `.ts` file were both honoured (statement count dropped from 5 to 4), so check your own pipeline and add `-- @preserve` if hints are ignored.

## 3. Thresholds that help
- Global thresholds fail CI on regressions; `thresholds.autoUpdate: true` rewrites `vitest.config.ts` with the new numbers when coverage exceeds them (a `lines: 10` threshold became `33.33` after one run). A per-glob entry such as `"src/a.ts": { lines: 95 }` failed with `does not meet "src/a.ts" threshold (95%)`.
- Per-glob thresholds for critical code: `thresholds: { "src/billing/**": { lines: 95 } }`.
- Diff/patch coverage in PRs (Codecov/Coveralls from `lcov.info`) is more useful than a global number.

## 4. E2E coverage
- Chromium: Playwright `page.coverage.startJSCoverage()` gives raw V8 data; convert with `v8-to-istanbul` / `monocart-reporter`.
- Or instrument the dev build with `vite-plugin-istanbul` and collect `window.__coverage__` after each test, then merge with `nyc merge`.

## Gotchas
- 100% line coverage with no assertions proves nothing; review tests, consider mutation testing (Stryker) for core logic.
- Coverage slows runs; enable it in CI and on demand locally, not in watch mode.

## Verify
- [ ] Removing a test drops coverage below the threshold and CI fails.
- [ ] HTML report (`coverage/index.html`) lists files with 0% that you expected to be tested.
