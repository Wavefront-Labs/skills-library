---
id: computing-software.qa-testing-engineering.cypress.environment-variables-and-multiple-environments
name: environment-variables-and-multiple-environments
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-env, environment-variables, cypress-config, multiple-environments, baseurl]
level: practitioner
status: verified
description: "Configure Cypress 16 for multiple environments: cy.env and Cypress.expose precedence, CYPRESS_ vars, --env, --expose, per-environment config, secrets out of logs."
sources:
  - https://docs.cypress.io/app/guides/environment-variables
  - https://docs.cypress.io/app/references/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables and multiple environments (Cypress)

## Two APIs since Cypress 16.0.0
`Cypress.env()` was removed in 16.0.0 (calling it throws "`Cypress.env()` was removed in Cypress version 16.0.0"; on 15.x it printed a deprecation warning controlled by `allowCypressEnv`). Replacements (both introduced in the 15.x line):
- `cy.env(['KEY', ...])` yields `{ KEY: value }` for secrets. Values stay in the Node process until requested. Sources, later wins: `env` in the config file, then `cypress.env.json` (git-ignored), then OS vars prefixed `CYPRESS_` (`CYPRESS_foo=...` gives `foo`; prefixed vars matching config keys such as `CYPRESS_BASE_URL` set config instead), then CLI `--env a=1,flag=true`. A local run gave `layered` = config, envjson, os, cli in that order. Numbers and booleans from `--env` arrive typed (`n=5` gave a number, `flag=true` a boolean).
- `Cypress.expose('key')` reads public, non-sensitive values from the `expose` config object or `--expose a=1,b=2` (CLI wins over config). They are visible to the app under test.
- Per-test or per-suite overrides: `{ env: ... }` now throws ("Overriding the `env` configuration was removed in Cypress version 16.0.0"); use `describe('x', { expose: { feature: 'on' } }, ...)` instead (suite-level expose overrides applied to the tests in that suite).

## One config, environment selected at run time
```js
// cypress.config.js
const envs = {
  local:   { baseUrl: 'http://localhost:3000',            env: { apiUrl: 'http://localhost:8080' } },
  staging: { baseUrl: 'https://staging.example.test',      env: { apiUrl: 'https://api.staging.example.test' } },
};
module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      const target = envs[config.env.target || 'local'];   // config.env still holds --env values here
      return { ...config, baseUrl: target.baseUrl, env: { ...config.env, ...target.env } };
    },
  },
});
```
```bash
npx cypress run --env target=staging
CYPRESS_PASSWORD=$STAGING_PW npx cypress run --env target=staging   # read in tests with cy.env(['PASSWORD'])
```
Alternative: separate `--config-file cypress.staging.config.js` files extending a base.

## Secrets
- Inject from CI secret store as `CYPRESS_*`; never commit `cypress.env.json`.
- `{ log: false }` on `type`/`request` with secrets; videos and screenshots can capture typed values.
- `Cypress.expose()` values (and, on 15.x, `Cypress.env()` values) are visible to app code in the browser under test; keep production secrets out of them entirely and read secrets with `cy.env()`.

## Gotchas
- Changes made in `setupNodeEvents` must be returned in the config object; the `--env target=staging` example above switched `baseUrl` to the staging URL in a local run.
- Cypress 15.x projects: `allowCypressEnv: false` turns `Cypress.env()` off ahead of the 16 upgrade (the option is gone in 16).

## Verify
The same specs run against local and staging by switching one flag, and no secret appears in committed files or logs.
