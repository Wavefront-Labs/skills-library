---
id: computing-software.software-engineering.typescript.test-coverage-with-v8-and-istanbul
name: test-coverage-with-v8-and-istanbul
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, vitest-coverage, istanbul, v8-coverage, c8, coverage-thresholds, typescript-testing]
level: practitioner
status: verified
description: "Measure JS/TS coverage: Vitest and Jest with v8 or istanbul providers, include/all-files settings, thresholds and per-file gates, node --test coverage, and reading branch gaps."
sources: ["https://vitest.dev/guide/coverage", "https://jestjs.io/docs/configuration#coverageprovider-string", "https://nodejs.org/api/test.html#collecting-code-coverage", "https://istanbul.js.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test coverage with v8 and istanbul

**Goal:** honest coverage numbers (including untested files) wired into CI as a
regression gate.

## Providers
| Provider | How | Notes |
|---|---|---|
| `v8` | V8's built-in coverage, remapped via source maps | fast, no instrumentation; Vitest uses AST-aware remapping for accuracy |
| `istanbul` | instruments code before running | slower, mature, precise branch counting |

## Vitest
```ts
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],              // also reports files no test imports
      exclude: ["src/**/*.d.ts", "src/**/index.ts", "src/generated/**"],
      reporter: ["text", "html", "lcov", "json-summary"],
      thresholds: { lines: 80, branches: 75, functions: 80, statements: 80, perFile: false },
    },
  },
});
```
```bash
npm i -D @vitest/coverage-v8
npx vitest run --coverage
```
Without `include`, files never imported by tests are missing from the report and inflate the
percentage (tested: an unimported `mailer.ts` showed as 0% once `include` was set). `thresholds.autoUpdate: true` ratchets thresholds upward as coverage improves (tested: it rewrote `lines: 80` to `lines: 100` in the config file, so commit that file deliberately).

## Jest
```js
module.exports = {
  collectCoverage: true,
  coverageProvider: "v8",                 // default "babel" (istanbul), per the Jest configuration docs
  collectCoverageFrom: ["src/**/*.{ts,tsx}", "!src/**/*.d.ts"],
  coverageThreshold: { global: { branches: 75, lines: 80 } },
};
```

## Node's built-in runner
```bash
node --test --experimental-test-coverage --test-coverage-include='src/**' --test-coverage-lines=80
```
(Flags confirmed in `node --help` on Node 24.22 and run there; `--experimental-test-coverage` is still flagged as experimental.)
Or `c8 node --test` for istanbul-style reports.

## Ignoring code
`/* v8 ignore next */`, `/* v8 ignore start */ ... /* v8 ignore stop */`, or
`/* istanbul ignore next */`. Comments may be stripped by esbuild unless written as legal
comments (`/* v8 ignore next -- @preserve */`, per the Vitest coverage guide; tested: the hint removed the uncovered line). Justify every ignore.

## Reading reports
Open `coverage/index.html`: red lines never ran; yellow `E`/`I` markers show untaken
else/if branches. Branch coverage gaps on error paths are the most valuable to close.

## CI
Upload `lcov.info` to Codecov/Sonar for diff coverage on PRs; gate on "new code coverage"
rather than chasing a global number.

## Verify
- [ ] `include` configured so untested files count as 0%.
- [ ] Threshold failure breaks CI; ignore comments reviewed.
