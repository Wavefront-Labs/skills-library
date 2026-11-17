---
id: computing-software.qa-testing-engineering.cypress.mochawesome-and-junit-reporters
name: mochawesome-and-junit-reporters
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [mochawesome, cypress-reporters, junit-reporter-cypress, cypress-multi-reporters, report-merging]
level: practitioner
status: verified
description: "Configure Cypress reporters (spec, junit, mochawesome), combine them with cypress-multi-reporters, and merge per-spec JSON into one HTML report."
sources:
  - https://docs.cypress.io/app/tooling/reporters
  - https://github.com/adamgruber/mochawesome
  - https://www.npmjs.com/package/cypress-multi-reporters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reporters (mochawesome, junit) and merging

Cypress uses Mocha reporters and runs **each spec separately**, so file-based reporters write one file per spec. Use `[hash]` in filenames and merge afterwards.

## JUnit
```js
reporter: 'junit',
reporterOptions: { mochaFile: 'results/junit-[hash].xml', toConsole: false, testCaseSwitchClassnameAndName: false },
```

## Multiple reporters
```bash
npm i -D cypress-multi-reporters mocha-junit-reporter mochawesome mochawesome-merge mochawesome-report-generator
```
```js
reporter: 'cypress-multi-reporters',
reporterOptions: {
  reporterEnabled: 'spec, mocha-junit-reporter, mochawesome',
  mochaJunitReporterReporterOptions: { mochaFile: 'results/junit/[hash].xml' },
  mochawesomeReporterOptions: { reportDir: 'results/mochawesome', overwrite: false, html: false, json: true },
},
```

## Merge mochawesome
```bash
npx mochawesome-merge "results/mochawesome/*.json" > results/merged.json
npx marge results/merged.json --reportDir results/html --inline
```
Screenshots in the HTML need `cypress-mochawesome-reporter` (adds screenshots via `addContext`) or custom context; that package also wraps merging into one plugin.

## CI consumption
- JUnit files: point your CI's JUnit test-report feature at `results/junit/*.xml` (see your CI's documentation for the exact keyword; not checked here).
- Clean `results/` before each run (a `pre` script; `rm -rf` is POSIX-only, so use a cross-platform delete tool on Windows), or stale files from earlier runs get merged.

## Gotchas
- Without `[hash]`, each spec overwrites the previous file and the report shows only the last spec.
- `overwrite: false` + `html: false` for mochawesome per-spec JSON, otherwise multiple HTML files.

## Verify
Run on Cypress 16.2.0 with `cypress-multi-reporters`, `mocha-junit-reporter`, `mochawesome`, `mochawesome-merge`: three specs gave three `[hash].xml` files and `mochawesome.json`, `mochawesome_001.json`, `mochawesome_002.json`; the merge reported 5 tests, equal to the Cypress summary (3 + 1 + 1), and `marge ... --inline` wrote the HTML. Merged report test count equals Cypress run summary "Tests" total.
