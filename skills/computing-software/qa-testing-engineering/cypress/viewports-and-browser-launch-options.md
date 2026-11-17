---
id: computing-software.qa-testing-engineering.cypress.viewports-and-browser-launch-options
name: viewports-and-browser-launch-options
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cy-viewport, before-browser-launch, viewportwidth, browser-flags, cypress-browsers]
level: practitioner
status: verified
description: "Control Cypress viewport sizes (cy.viewport presets, config, per-test) and browser launch options (before:browser:launch args, prefs, extensions, headless)."
sources:
  - https://docs.cypress.io/api/commands/viewport
  - https://docs.cypress.io/api/node-events/browser-launch-api
  - https://docs.cypress.io/app/references/launching-browsers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Viewports and browser launch options

## Viewports
```js
// config: default 1000x660
e2e: { viewportWidth: 1280, viewportHeight: 800 }
cy.viewport('iphone-x'); cy.viewport('ipad-2', 'landscape'); cy.viewport(375, 667);
it('mobile nav', { viewportWidth: 375, viewportHeight: 667 }, () => { ... });
```
Responsive matrix:
```js
['iphone-6', 'ipad-2', [1440, 900]].forEach(size => {
  it(`header on ${size}`, () => { Array.isArray(size) ? cy.viewport(...size) : cy.viewport(size); cy.visit('/'); ... });
});
```
`cy.viewport` resizes the AUT iframe only; it does not emulate touch, user agent or device pixel ratio.

## Browser selection
`npx cypress run --browser <name-or-path>` (help text: a browser name, or a filesystem path to a binary); `--headed` / `--headless` (headless is the default in run mode). Electron is the default and is deprecated as a test browser since Cypress 16 (a warning prints each run); `--browser edge` worked here with Edge installed.

## before:browser:launch
```js
on('before:browser:launch', (browser, launchOptions) => {
  if (browser.family === 'chromium' && browser.name !== 'electron') {   // Electron is family 'chromium' too, but has no preferences.default
    launchOptions.args.push('--window-size=1920,1080', '--force-device-scale-factor=1', '--lang=de-DE');
    launchOptions.preferences.default.intl = { accept_languages: 'de-DE' };
  }
  if (browser.name === 'electron') launchOptions.preferences.width = 1920;
  launchOptions.extensions.push('/path/to/unpacked-ext');   // documented: folders of unpacked WebExtensions (not run here)
  return launchOptions;
});
```
In Electron, failure screenshots were 1280x720 while `cy.screenshot()` of the AUT matched the 1000x660 viewport. In Edge, `--window-size=1920,1080` produced 1896x988 failure screenshots (browser chrome is subtracted), and `--lang=de-DE` made `navigator.language` `de-DE`; set the window size explicitly for consistent screenshots.

## Gotchas
- WebKit support is experimental: `experimentalWebKitSupport: true` plus the `playwright-webkit` package (launching-browsers docs). `args` has no effect on Electron (before:browser:launch docs); Electron options go in `preferences` (e.g. `width`, `devTools`).
- Chrome flags change between versions; verify with `chrome://version` in `cypress open`.

## Verify
Run on Cypress 16.2.0 in Electron and Edge 155: default viewport 1000x660, `iphone-x` 375x812, `ipad-2` landscape 1024x768, test-config viewport 375, `cy.viewport` leaving the user agent and device pixel ratio (1) unchanged, `before:browser:launch` options applied. Screenshots in CI have the expected dimensions; mobile tests render the hamburger menu.
