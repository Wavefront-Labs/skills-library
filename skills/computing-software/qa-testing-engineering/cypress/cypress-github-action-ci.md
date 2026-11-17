---
id: computing-software.qa-testing-engineering.cypress.cypress-github-action-ci
name: cypress-github-action-ci
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-github-action, github-actions, cypress-ci, wait-on, cypress-cache]
level: practitioner
status: verified
description: "Run Cypress in GitHub Actions with cypress-io/github-action: install caching, start and wait-on the app, browsers, artifacts upload, component tests and containers."
sources:
  - https://github.com/cypress-io/github-action
  - https://docs.cypress.io/app/continuous-integration/github-actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Cypress in GitHub Actions

```yaml
name: e2e
on: [pull_request]
jobs:
  cypress:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v7
      - uses: cypress-io/github-action@v7
        with:
          build: npm run build
          start: npm run preview
          wait-on: 'http://localhost:4173'
          wait-on-timeout: 120
          browser: chrome
          config: video=false
      - uses: actions/upload-artifact@v7
        if: failure()
        with: { name: cypress-screenshots, path: cypress/screenshots, if-no-files-found: ignore }
```

## What the action does
- Installs deps with the command matching the lockfile (`npm ci`, `yarn --frozen-lockfile`, `pnpm install --frozen-lockfile`) and caches the package manager's cache and the Cypress binary (README "Caching"; disable with `package-manager-cache: false`, custom key with `cache-key`).
- Verifies the binary, optionally builds, starts the server in the background, waits for URLs, runs `cypress run`.
- `install: false` on later steps to reuse an earlier install (e.g. run e2e then component).
- `component: true` runs component tests.
- `working-directory` for monorepos; `command` overrides `cypress run` (`command-prefix` prefixes it). Other inputs in `action.yml`: `browser`, `config`, `config-file`, `env`, `expose`, `spec`, `record`, `parallel`, `group`, `tag`, `headed`, `quiet`, `start`, `wait-on`, `wait-on-timeout` (default wait is 60 s per the README), `build`, `install-command`.
- Current release at check time: v7.4.6 (`action.yml` runs on `node24`); the README examples use `actions/checkout@v7` and `ubuntu-26.04`; `ubuntu-24.04` is also a valid runner label.

## Containers
Use `container: cypress/browsers:latest` (pin a tag) for consistent browser versions; add `options: --user 1001` to avoid permission issues with the GitHub workspace.

## Gotchas
- Match the `wait-on` URL to the host and port your server binds (for example `http://127.0.0.1:4173` when the server listens on IPv4 only).
- Upload videos/screenshots with `if: failure()` (or `always()`) or they're lost.

## Verify
Inputs, container advice and defaults above were checked against the action's `action.yml` and README on GitHub (the workflow itself was not run: GitHub Actions is not available to this reviewer). Second run logs a cache hit for the Cypress binary; failing tests upload screenshots.
