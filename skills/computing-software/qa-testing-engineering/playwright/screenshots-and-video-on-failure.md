---
id: computing-software.qa-testing-engineering.playwright.screenshots-and-video-on-failure
name: screenshots-and-video-on-failure
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-video, screenshot-on-failure, test-artifacts-playwright, outputdir]
level: practitioner
status: docs-checked
description: "Configure Playwright screenshot, video and trace capture modes (on, off, only-on-failure, retain-on-failure), video size, outputDir, and manual screenshots."
sources:
  - https://playwright.dev/docs/api/class-testoptions
  - https://playwright.dev/docs/videos
  - https://playwright.dev/docs/screenshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Screenshots and video on failure

**Goal:** enough evidence for every CI failure, without gigabytes of artifacts for passing tests.

## Config
```ts
use: {
  screenshot: 'only-on-failure',     // 'off' | 'on' | 'only-on-failure' | 'on-first-failure' (or { mode, fullPage, omitBackground })
  video: 'retain-on-failure',        // 'off' | 'on' | 'retain-on-failure' | 'on-first-retry' | 'on-all-retries' | 'retain-on-first-failure' | 'retain-on-failure-and-retries'
  trace: 'on-first-retry',
},
outputDir: 'test-results',           // default; unique per-test subfolders; cleaned at the start of each run
```
Video size: `video: { mode: 'retain-on-failure', size: { width: 1280, height: 720 } }` (the default is the viewport size scaled down to fit 800x800).

## Manual captures
```ts
await page.screenshot({ path: testInfo.outputPath('step3.png'), fullPage: true });
await page.getByRole('dialog').screenshot({ path: 'dialog.png' });
const buf = await page.screenshot();
await testInfo.attach('after-submit', { body: buf, contentType: 'image/png' });
```
The video is only available after the page or browser context is closed; read its path with `await page.video().path()` after that.

## Library mode
```ts
const context = await browser.newContext({ recordVideo: { dir: 'videos/', size: { width: 1280, height: 720 } } });
```

## Choosing modes
- Traces include DOM snapshots, network and console; video shows what happened on screen.
- `retain-on-failure` records every run and keeps the video only for failures; `on-first-retry` records only the first retry.

## Gotchas
- `outputDir` is wiped at run start: copy artifacts elsewhere before a second run in the same CI job.
- Upload `test-results/` and `playwright-report/` in CI with a condition such as `!cancelled()` so failures are still uploaded.

## Verify
A deliberately failing test has a screenshot and a video attached in the HTML report.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the screenshot modes (off, on, only-on-failure, on-first-failure) and fullPage and omitBackground options, the video modes and size option, the default video size rule (viewport scaled to fit 800x800), recordVideo in library mode, page.video().path() being available only after the page or context closes, outputDir defaulting to test-results and being cleaned at the start of a run, and the trace modes. Removed: the CPU cost remark, the file-name and WebM statements, which the docs do not state.

Method: documentation only; no commands were run.
