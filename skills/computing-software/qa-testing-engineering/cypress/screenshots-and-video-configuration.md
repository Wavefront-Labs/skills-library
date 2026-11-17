---
id: computing-software.qa-testing-engineering.cypress.screenshots-and-video-configuration
name: screenshots-and-video-configuration
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-video, cypress-screenshots, cypress-config, ci-artifacts, test-evidence]
level: practitioner
status: verified
description: "Configure Cypress screenshots and video: automatic failure screenshots, cy.screenshot options, video opt-in and compression, folders, trashing, and uploading CI artifacts."
sources:
  - https://docs.cypress.io/app/guides/screenshots-and-videos
  - https://docs.cypress.io/api/commands/screenshot
  - https://docs.cypress.io/app/references/configuration#Videos
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Screenshots and video configuration (Cypress)

## Config
```js
module.exports = defineConfig({
  screenshotOnRunFailure: true,              // default true in run mode
  screenshotsFolder: 'cypress/screenshots',
  video: true,                               // default false since Cypress 13
  videoCompression: 32,                      // CRF 0-51; true = 32; false to skip compression (faster)
  videosFolder: 'cypress/videos',
  trashAssetsBeforeRuns: true,
  viewportWidth: 1280, viewportHeight: 720,
});
```
Video records only in `cypress run` (an `.mp4` per spec appeared in `cypress/videos` with Electron; other browsers were not tried). `video` and `videoCompression` both default to `false` since Cypress 13.0.0.

## Keep only failing videos
```js
setupNodeEvents(on) {
  on('after:spec', (spec, results) => {
    if (results && results.video) {
      const failed = results.tests.some((t) => t.attempts.some((a) => a.state === 'failed'));
      if (!failed) require('fs').unlinkSync(results.video);
    }
  });
}
```

## Manual screenshots
```js
cy.screenshot('checkout-summary', { capture: 'viewport' });   // fullPage (default) | viewport | runner
cy.get('[data-cy=invoice]').screenshot('invoice', { padding: 10, blackout: ['[data-cy=timestamp]'] });
```
Failure screenshots are named `<spec file>/<suite> -- <test title> (failed).png` (e.g. `cypress/screenshots/fail2.cy.js/f -- a (failed).png`). `cy.screenshot()` defaults to `capture: 'fullPage'`; the `after:screenshot` handler receives `path`, `name`, `specName`, `testFailure`, `takenAt`, `dimensions` and others, and returning `{ path }` only updates the reported path: the handler must move the file itself (`fs.renameSync`), otherwise the file keeps its name.

## CI upload (GitHub Actions)
```yaml
- uses: actions/upload-artifact@v7
  if: failure()
  with:
    name: cypress-artifacts
    path: |
      cypress/screenshots
      cypress/videos
```

## Gotchas
- Video encoding adds time per spec; compress less or record only on CI where needed.
- Screenshots and videos may contain secrets or personal data typed during tests; use `{ log: false }` and test data.
- `cy.screenshot` is not a visual regression test; use a visual diff tool for that.

## Verify
Run on Cypress 16.2.0: failure screenshots, manual full/element screenshots with `padding`/`blackout`, the `.mp4` video, and `after:spec` deleting the video of a passing spec (the failing spec's video stayed). Failed CI runs upload screenshots and videos, passing specs leave no video, and artifact size stays bounded.
