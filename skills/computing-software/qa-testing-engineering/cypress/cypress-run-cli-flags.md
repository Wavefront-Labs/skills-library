---
id: computing-software.qa-testing-engineering.cypress.cypress-run-cli-flags
name: cypress-run-cli-flags
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-cli-flags, cypress-run-command, cypress-spec-filter, record-key, cypress-env-flag]
level: practitioner
status: verified
description: "Run Cypress from the CLI with the right flags: --spec globs, --browser, --config, --env, --record/--key/--parallel/--group/--tag, --quiet, exit codes."
sources:
  - https://docs.cypress.io/app/references/command-line
  - https://docs.cypress.io/app/references/module-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cypress run CLI flags

```bash
npx cypress run                                         # all e2e specs, Electron (deprecated since 16), headless
npx cypress run --spec "cypress/e2e/checkout/**/*.cy.ts" --browser chrome
npx cypress run --component                             # component tests
npx cypress run --config baseUrl=https://staging.test,video=false
npx cypress run --env environment=staging               # read with cy.env(['environment'])
npx cypress run --expose grepTags=@smoke                # public values: Cypress.expose('grepTags')
npx cypress run --config-file cypress.staging.config.js
npx cypress run --record --key $CYPRESS_RECORD_KEY --parallel --group "chrome-e2e" --ci-build-id $GITHUB_RUN_ID --tag nightly
npx cypress run --reporter junit --reporter-options "mochaFile=results/junit-[hash].xml"
npx cypress run --quiet --headed --no-exit                # debugging
```

## Exit codes
- `0`: all passed. `N`: number of failed tests (two failures exited 2 in a local run). Non-zero on config/startup errors too (a glob matching no spec exited 1).
- `--posix-exit-codes` exists for POSIX-style codes (two failures exited 1 with it).
- The browser closes after the run; `--no-exit` keeps it open.
CI should treat any non-zero as failure; scripts that compare to `1` miss multi-failure runs.

## Env var equivalents
`CYPRESS_BASE_URL`, `CYPRESS_RECORD_KEY`; config keys map too (`CYPRESS_VIDEO=false`). Any other `CYPRESS_foo` becomes env var `foo`, read with `cy.env(['foo'])` on Cypress 16 (`Cypress.env()` was removed in 16.0.0; it was `Cypress.env('foo')` before).

## Module API (programmatic)
```js
const cypress = require('cypress');
const results = await cypress.run({ spec: 'cypress/e2e/smoke/*.cy.js', browser: 'chrome', config: { video: false } });
// on a run that could not start, results is { status: 'failed', failures, message }; on a finished run status is undefined and totalFailed counts failures
if (results.status === 'failed' || results.totalFailed) process.exit(1);
```

## Gotchas
- Quote spec globs, or the shell expands them.
- `--parallel` (and `--group`, `--tag`, `--ci-build-id`) without `--record` is rejected by the CLI; parallel balancing needs Cypress Cloud or a third-party orchestrator.
- Cypress 16 needs Node `^22`, `^24` or `>=26`.
- `--config` comma-separated values cannot contain commas; use `--config-file` or JSON: `--config '{"retries":{"runMode":2}}'`.

## Verify
`npx cypress run --spec <one spec>` in CI produces a JUnit file per spec with unique names (two specs gave two `junit-<hash>.xml` files). Flags above checked against `npx cypress run --help` on Cypress 16.2.0; the flag names for recorded runs come from that help text (Cloud behaviour is out of scope here).
