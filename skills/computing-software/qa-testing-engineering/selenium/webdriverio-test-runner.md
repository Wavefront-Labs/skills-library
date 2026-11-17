---
id: computing-software.qa-testing-engineering.selenium.webdriverio-test-runner
name: webdriverio-test-runner
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium, webdriverio, selenium-framework, wdio, mocha, javascript, typescript, webdriver-bidi]
level: practitioner
status: docs-checked
description: "Set up WebdriverIO: wdio.conf configuration, services and reporters, selectors and auto-waiting commands, page objects and running against Selenium Grid or cloud."
sources:
  - https://webdriver.io/docs/gettingstarted
  - https://webdriver.io/docs/configuration
  - https://webdriver.io/docs/selectors
  - https://github.com/webdriverio/webdriverio/tree/main/website/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebdriverIO test runner

**Goal:** a JavaScript/TypeScript WebDriver framework with batteries included (runner, waits, services, reporters).

## Setup
```bash
npm init wdio@latest .      # wizard: framework (mocha/jasmine/cucumber), reporters, services
npx wdio run wdio.conf.ts
```

## Config essentials (wdio.conf.ts)
```ts
export const config: WebdriverIO.Config = {
  specs: ['./test/specs/**/*.ts'],
  maxInstances: 5,                           // total parallel workers (default 100)
  capabilities: [{ browserName: 'chrome', 'goog:chromeOptions': { args: ['--headless=new'] } },
                 { browserName: 'firefox' }],
  baseUrl: 'http://localhost:3000',
  waitforTimeout: 10000,                     // waitFor* commands only (default 5000)
  framework: 'mocha', mochaOpts: { timeout: 60000 },
  reporters: ['spec', ['junit', { outputDir: './results' }], ['allure', { outputDir: 'allure-results' }]],
  // Grid/cloud: hostname, port, path, or services: ['browserstack'] / ['sauce']
}
```

## Test
```ts
describe('checkout', () => {
  it('applies gold discount', async () => {
    await browser.url('/basket')
    await $('aria/Apply discount').click()       // accessibility-name selector
    await expect($('[data-testid="total"]')).toHaveText('90.00')   // auto-retrying matcher
  })
})
```
Selectors: CSS, `aria/name`, `=Link text`, `*=partial`, `react$('Component')`. Since v9 WebdriverIO pierces the Shadow DOM automatically, so the old `>>>` deep selector is no longer needed.

## Notes
- Commands automatically wait for elements to become interactable; `expect-webdriverio` matchers retry until timeout.
- By default WebdriverIO attempts a WebDriver BiDi session (set `wdio:enforceWebDriverClassic` to opt out); mock network via `browser.mock(...)`.
- Page objects as classes with getters returning `$()`.

## Gotchas
- The sync mode has been removed: always `await` commands.
- `maxInstances` and per-capability `wdio:maxInstances` limit parallel sessions; keep them within your Grid or cloud plan capacity.

## Verify
Run on two capabilities in parallel; JUnit and Allure outputs generated per capability.

## Checked

Checked 2026-10-25 against the WebdriverIO documentation source (webdriverio/webdriverio website/docs, main branch, pushed 2026-10-25, v9 era). Confirmed: `npm init wdio@latest .`, `npx wdio run wdio.conf.ts`, `WebdriverIO.Config`, `maxInstances` (default 100) and `wdio:maxInstances`, `waitforTimeout` (default 5000, `waitFor*` only), `baseUrl`, `mochaOpts`, reporters `junit` and `allure`, `services: ['sauce']` and `'browserstack'`, selectors `aria/`, `=`, `*=`, `react$`, `browser.mock`, `expect-webdriverio` matchers, automatic BiDi attempt and `wdio:enforceWebDriverClassic`, removal of sync mode. Corrected: the `>>>` deep selector is unnecessary since v9. Added the documented `wdio:enforceWebDriverClassic` opt-out. Removed: the unsupported removal-version claim ('v8') and the Grid-queueing claim.

Method: documentation only; no commands were run.
