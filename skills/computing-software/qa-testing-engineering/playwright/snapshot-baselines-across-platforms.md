---
id: computing-software.qa-testing-engineering.playwright.snapshot-baselines-across-platforms
name: snapshot-baselines-across-platforms
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [update-snapshots, snapshot-path-template, visual-regression, playwright-screenshots, docker-baselines]
level: practitioner
status: docs-checked
description: "Manage Playwright screenshot baselines across OS and browsers: snapshotPathTemplate, updating in Docker for CI parity, thresholds, masks, and reviewing baseline changes."
sources:
  - https://playwright.dev/docs/test-snapshots
  - https://playwright.dev/docs/api/class-testconfig#test-config-snapshot-path-template
  - https://playwright.dev/docs/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing snapshot baselines across platforms

**Goal:** visual baselines that match what CI renders, update in one command, and are reviewable.

## Why platform matters
Screenshots differ between browsers and platforms because of rendering, fonts and more, so snapshot names include the browser (project) and the platform (for example `example-test-1-chromium-darwin.png`). A baseline generated on macOS is not used on Linux CI.

## Path template
```ts
export default defineConfig({
  snapshotPathTemplate: '{testDir}/__screenshots__/{testFilePath}/{arg}-{projectName}{ext}',
  expect: { toHaveScreenshot: { maxDiffPixelRatio: 0.01, animations: 'disabled', caret: 'hide' } },
});
```
Dropping `{platform}` is safe only if baselines are always generated in the same Linux container.

## Generate/update in the CI image
```bash
docker run --rm --ipc=host -v "$(pwd)":/work -w /work mcr.microsoft.com/playwright:v<version>-noble \
  npx playwright test --update-snapshots --grep @visual
```
Match the image tag to the installed `@playwright/test` version. Update modes: `--update-snapshots=all|changed|missing|none|default`; without a value the flag means `changed`, and running without the flag means `default`.

## Stabilise screenshots
- `mask: [page.getByTestId('timestamp')]`, `stylePath` to hide dynamic regions.
- Freeze time (`page.clock.setFixedTime`) and seed data.

## Review workflow
- Baselines committed with the change that caused them; reviewers inspect images in the PR diff.
- A CI job (manual trigger) can regenerate baselines and push to the branch.

## Gotchas
- `--update-snapshots` locally on a Mac produces `-darwin` files that CI ignores; generate in Docker.
- Large thresholds hide real regressions; prefer masks over raising thresholds.

## Verify
CI and local Docker runs produce identical baselines, and a 1 px intentional style change fails then passes after an update.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: that snapshot names include the browser and platform, the snapshotPathTemplate tokens ({testDir}, {testFilePath}, {arg}, {projectName}, {platform}, {ext}) and per-assertion pathTemplate under expect, the --update-snapshots modes and their defaults, --ipc=host and version-matched image tags for Docker, mask and stylePath, and page.clock.setFixedTime. Removed: the 1.50+ version gate, the host-network flag, the fonts.ready and viewport tips, and the diff-slider claim, which the docs do not state.

Method: documentation only; no commands were run.
