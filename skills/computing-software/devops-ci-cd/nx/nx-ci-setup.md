---
id: computing-software.devops-ci-cd.nx.nx-ci-setup
name: nx-ci-setup
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, ci, github-actions, nx-affected, nx-set-shas, ci-workflow, nx-cloud]
level: intro
status: docs-checked
description: "Set up CI for an Nx workspace: nx init, ci-workflow generator and --ci values, affected with nx-set-shas, then remote cache and workers; full GitHub Actions example."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/getting-started/setup-ci.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a CI pipeline that runs only affected tasks through Nx, then adds caching and distribution.

Install Nx: existing repo `npx nx@latest init`; new repo `npx create-nx-workspace@latest`.

Rule: caching, affected and distribution apply only to tasks Nx runs. `nx test`, or `npm test` wrapping it, is fine; direct `jest`, `tsc` or `eslint` calls skip Nx.

Generate a workflow if none exists:
```shell
nx add @nx/workspace
nx g @nx/workspace:ci-workflow --ci=github
```
`--ci` accepts `github`, `circleci`, `gitlab`, `azure`, `bitbucket-pipelines`. The output already includes the Nx Cloud steps.

Connect Nx Cloud (remote cache): `npx nx-cloud onboard connect-workspace` prints JSON; confirm `nxCloudId` was written to `nx.json`, and if the response has an `actionRequired` payload (typically GitHub authorization), stop and surface it. Read-only vs read-write CI tokens: see nx-remote-cache.

Complete GitHub Actions example:
```yaml
# .nx/ci-config.yaml
dte:
  distribute-on: 3 linux-large-js
lifecycle:
  stop-after:
    - build
```
```yaml
# .github/workflows/ci.yml
name: CI
on:
  push: { branches: [main] }
  pull_request:
permissions: { actions: read, contents: read }
jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with: { fetch-depth: 0, filter: tree:0 }
      - run: npx nx-cloud start-workers     # before installing deps so workers boot meanwhile
      - uses: actions/setup-node@v6
        with: { node-version: 24, cache: npm }
      - run: npm ci
      - uses: nrwl/nx-set-shas@v5           # base = last commit that passed CI on main
      - run: npx nx affected -t lint test build
```
`fetch-depth: 0` is needed so Nx can compare commits. On PRs the base is `main` or `defaultBase` in `nx.json`. There is no `--parallel` to set once workers run (nx-distributed-workers). Self-healing step: nx-self-healing-ci. Other providers: the CI workflow examples page.

## Checked

2026-11-07. Confirmed: the Set up CI flow, nxCloudId and actionRequired handling against the Set up CI page. Removed: npx nx@latest connect (not on that page; connect step now uses npx nx-cloud onboard connect-workspace) and an invented Verify step.

Method: documentation only; no commands were run.
