---
id: computing-software.web-development.storybook.tests-in-ci
name: tests-in-ci
category: computing-software
field: web-development
product: storybook
tags: [ci, github-actions, test-storybook-script, playwright-image, continuous-integration]
level: practitioner
status: docs-checked
description: "Run Storybook component tests in CI with a package script and a Playwright container."
sources:
  - https://storybook.js.org/docs/writing-tests/in-ci
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Storybook tests in CI

Goal: catch broken stories on every pull request.

1. Add a script:

```json
{ "scripts": { "test-storybook": "vitest --project=storybook" } }
```
Adjust the project name if you renamed it from `storybook`.

2. Add a workflow, for example GitHub Actions:

```yaml
name: UI Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright:v1.58.2-noble
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22.12.0
      - run: npm ci
      - run: npm run test-storybook
```

The page says to grab the latest Playwright image, since Storybook Test uses Playwright by default and an image with it preinstalled is fastest. The Vitest addon requires a Vite-based framework. The page also gives GitLab, Bitbucket, CircleCI, Travis, Jenkins and Azure examples that call the same script.

- Debug links: failure output links to the failing story, which in CI means a published Storybook. On GitHub, run on `deployment_status`, pass `deployment_status.environment_url` as `SB_URL`, and use it in the Vitest addon's `storybookUrl` option.
- Coverage: add `--coverage` to the script or to the CI command (`npm run test-storybook -- --coverage`).
- Other Vitest projects: run them with their own `--project` script, or omit the filter (`vitest`) to run everything together.

## Checked

Method: 2026-11-08 read docs/writing-tests/in-ci.mdx from the Storybook repo. The script and GitHub Actions example match the page. Removed an unsupported Chromatic cross-reference and "for free" claim and a Verify step; added SB_URL, coverage and project-filter guidance.
