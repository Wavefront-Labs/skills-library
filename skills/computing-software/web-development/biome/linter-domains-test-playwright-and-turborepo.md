---
id: computing-software.web-development.biome.linter-domains-test-playwright-and-turborepo
name: linter-domains-test-playwright-and-turborepo
category: computing-software
field: web-development
product: biome
tags: [biome, test-domain, playwright-domain, turborepo-domain, test-globals, no-focused-tests, no-skipped-tests, no-undeclared-env-vars, jest, vitest]
level: practitioner
status: docs-checked
description: "Test and tooling domains: recognised globals, recommended rules like noFocusedTests and noPlaywrightMissingAwait, and the Turborepo env-var rule."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/domains.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Test domain.** Library-agnostic rules for linting test files; enabled by `jest`, `mocha`, `ava` or `vitest` dependencies. When enabled these globals are recognised: `after`, `afterAll`, `afterEach`, `before`, `beforeEach`, `beforeAll`, `context`, `describe`, `it`, `expect`, `run`, `setup`, `specify`, `suite`, `suiteSetup`, `suiteTeardown`, `teardown`, `test`, `xcontext`, `xdescribe`, `xit`, `xspecify`.

Recommended test rules: `noDuplicateTestHooks`, `noExportsInTest`, `noFocusedTests`, `noIdenticalTestTitle`. Non-recommended examples: `noSkippedTests`, `noConditionalExpect`, `useExpect`, `useConsistentTestIt`, `useTestHooksInOrder`, `useTestHooksOnTop`, `noExcessiveNestedTestSuites`. Nursery: `useExpectToContain`, `useLowercaseTestTitle`, `useValidTestTitle`.

**Playwright domain.** Enabled by `@playwright/test` (>=1.0.0). Recognised globals: `test` and `expect`. Recommended rules: `noPlaywrightMissingAwait` and `usePlaywrightValidDescribeCallback`. Others (not recommended): `noPlaywrightUselessAwait`, `noPlaywrightElementHandle`, `noPlaywrightEval`, `noPlaywrightWaitForSelector`, `noPlaywrightForceOption`, `noPlaywrightNetworkidle`, `noPlaywrightPagePause`, `noPlaywrightWaitForNavigation`, `noPlaywrightWaitForTimeout`; nursery: `noPlaywrightNthMethods`, `noPlaywrightUnsafeReferences`.

**Turborepo domain.** Enabled by `turbo` (>=1.0.0); its one rule is the recommended `noUndeclaredEnvVars`.

**Drizzle domain.** Recommended: `noDrizzleDeleteWithoutWhere` and `noDrizzleUpdateWithoutWhere`.

Enable explicitly when auto-detection does not apply:

```json
{ "linter": { "domains": { "test": "recommended", "playwright": "recommended" } } }
```

Each domain accepts `"recommended"` (recommended, non-nursery rules), `"all"` or `"none"`. Drizzle is enabled by `drizzle-orm` (>=0.9.0). Test domain dependency minimums: `jest` >=26.0.0, `mocha` >=8.0.0, `ava` >=2.0.0, `vitest` >=1.0.0.

## Checked

Method: 2026-11-08 compared against the Biome website source mdx for linter domains (Drizzle, Playwright, Test, Turborepo sections). Globals, dependencies and rule lists match the page. Added the missing nursery rule noPlaywrightUnsafeReferences and the dependency minimums, dropped an unstated cross-reference to Turborepo skills, and dropped an invented "Verify" step.
