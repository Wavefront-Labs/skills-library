---
id: computing-software.qa-testing-engineering.jest-pytest.jest-config-testenvironment-projects
name: jest-config-testenvironment-projects
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [testenvironment, jest-projects, jest-config, jsdom, module-name-mapper]
level: practitioner
status: verified
description: "Configure Jest: testEnvironment (node, jsdom, per-file docblock), projects for multi-package or multi-environment runs, moduleNameMapper, transforms and coverage settings."
sources:
  - https://jestjs.io/docs/configuration
  - https://jestjs.io/docs/configuration#projects-arraystring--projectconfig
  - https://jestjs.io/docs/configuration#testenvironment-string
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jest config, testEnvironment and projects

## Core config
```js
// jest.config.js
/** @type {import('jest').Config} */
module.exports = {
  testEnvironment: 'node',                       // the default
  roots: ['<rootDir>/src'],
  testMatch: ['**/?(*.)+(spec|test).[jt]s?(x)'],
  moduleNameMapper: { '^@/(.*)$': '<rootDir>/src/$1', '\\.(css|scss)$': 'identity-obj-proxy' },   // identity-obj-proxy is a separate npm package
  setupFilesAfterEnv: ['<rootDir>/test/setup.ts'],
  clearMocks: true, restoreMocks: true,
  collectCoverageFrom: ['src/**/*.{ts,tsx}', '!src/**/*.d.ts'],
  coverageThreshold: { global: { branches: 80, lines: 85 } },
};
```

## testEnvironment
- `node`: server code, fastest.
- `jsdom`: DOM APIs; install `jest-environment-jsdom` separately (Jest 28+).
- Per file docblock overrides:
```js
/**
 * @jest-environment jsdom
 */
```
- Options: `testEnvironmentOptions: { url: 'https://app.test/' }`.

## projects
One run, several configs (monorepo or node + browser split):
```js
module.exports = {
  projects: [
    { displayName: 'server', testEnvironment: 'node', testMatch: ['<rootDir>/server/**/*.test.ts'] },
    { displayName: 'web', testEnvironment: 'jsdom', testMatch: ['<rootDir>/web/**/*.test.tsx'], setupFilesAfterEnv: ['<rootDir>/web/setup.ts'] },
    '<rootDir>/packages/*',          // each with its own jest.config
  ],
};
```
`npx jest --selectProjects web`. Each project is shown by its `displayName` in `npx jest --showConfig`. Project-level `globalSetup`/`globalTeardown` only run when at least one test from that project runs (Jest configuration docs).

## Useful CLI
`--runInBand` (debugging, DB tests), `--maxWorkers=50%`, `--shard=1/3`, `--changedSince=origin/main`, `--ci` (new snapshots are not written and the test fails with "New snapshot was not written"), `--silent`.

## Gotchas
- Misspelled keys (e.g. `setupFilesAfterEach` for `setupFilesAfterEnv`) only produce an "Unknown option" validation warning, so the setup never runs; read the warnings and check `npx jest --showConfig`.
- jsdom lacks layout (`getBoundingClientRect` returns zeros), `matchMedia`, `IntersectionObserver` (all confirmed on jest-environment-jsdom 30): mock them in setup.
- `moduleNameMapper` regexes are anchored per your pattern; order matters (first match wins; ran with `^foo/(.*)$` listed before `^foo/bar$`).

## Verify
`npx jest --showConfig` shows the resolved per-project settings; `--listTests` lists expected files.
