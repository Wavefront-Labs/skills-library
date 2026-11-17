---
id: computing-software.software-engineering.mobile-development.detox-e2e-testing
name: detox-e2e-testing
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, detox, e2e, end-to-end-testing, grey-box-testing, simulator-testing, android-emulator, detoxrc, jest-integration, device-configuration, test-ids, mobile-testing, flakiness, ui-automation]
level: practitioner
status: docs-checked
description: "Run grey-box end-to-end tests with Detox: .detoxrc.js devices/apps/configurations, config search order, waitFor with withTimeout, and the multi-app configuration."
sources: ["https://wix.github.io/Detox/docs/introduction/getting-started/", "https://wix.github.io/Detox/docs/config/overview/", "https://wix.github.io/Detox/docs/api/device", "https://wix.github.io/Detox/docs/api/expect/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detox: grey-box end-to-end testing

**Goal:** drive the real app on a real device or simulator and assert on the UI, without the flakiness of
black-box testers.

Detox (Detox 20.x docs) is an open-source end-to-end framework for React Native apps. Black-box UI frameworks have no
access to app internals and are unaware of asynchronous operations (network requests, animations), which makes tests
flaky. Detox takes a "gray box" approach, with access to the internals of the app under test, for more control and
predictability.

A test:

```js
describe('Login flow', () => {
  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should login successfully', async () => {
    await element(by.id('email')).typeText('john@example.com');
    await element(by.id('password')).typeText('123456');
    const loginButton = element(by.text('Login'));
    await loginButton.tap();
    await expect(loginButton).not.toExist();
    await expect(element(by.label('Welcome'))).toBeVisible();
  });
});
```

Matchers shown: `by.id`, `by.text`, `by.label`.

## Configuration
Detox prefers static configuration describing permutations of apps and devices. Even a simple React Native app has four
combinations: iOS simulator debug and release, Android emulator debug and release. Keep configs in three dictionaries,
`devices`, `apps` and `configurations`:

```js
/* @type {Detox.DetoxConfig} */
module.exports = {
  devices: { device1: { /* ... */ } },
  apps: { app1: { /* ... */ } },
  configurations: {
    'device1+app1': { device: 'device1', app: 'app1' },
  },
};
```
Run one with `detox test -c 'device1+app1'`.

- Other sections: `artifacts`, `behavior`, `logger`, `session`, `testRunner`. Each configuration can override these
  global sections (for example `testRunner.args.runInBand` or `logger.level`).
- Aliasing is optional: a configuration can inline `device` (for example `type: 'ios.simulator'`,
  `device: { type: 'iPhone 13 Pro' }`) and `app` (`type: 'ios.app'`, `binaryPath`).
- **Multi-app** tests have basic support: use `apps: [...]` (aliased or inlined) instead of `app`.
- Config search starts at the current working directory and runs in this order: `.detoxrc.js`, `.detoxrc.json`,
  `.detoxrc` (JSON), `detox.config.js`, `detox.config.json`, then a top-level `detox` key in `package.json`.
- `extends` takes a Node module path (relative paths resolve from the config file that contains it); chains are
  deep-merged grandparent, parent, child.
- You can omit `-c` if there is only one configuration or `selectedConfiguration` names a default.

## Device and waiting
- `device.reloadReactNative()` reloads the JS bundle and is much faster than `device.launchApp()`, but the docs warn it
  may misbehave or crash under some conditions; then use `device.launchApp()` for a clean launch.
- `launchApp` accepts parameters such as `newInstance`, `permissions` and `url`.
- Wait for conditions with `await waitFor(element(by.id('bigButton'))).toBeVisible().withTimeout(2000);`.

## Verify
- [ ] Each platform and build type you ship has a configuration entry.
- [ ] Multi-app flows declare an `apps` array, not a single `app`.
- [ ] The suite passes repeatedly in CI without fixed sleeps.

## Checked
2026-11-08. Confirmed against the Detox 20.x pages Getting Started, Config Overview, device API and expect API: gray-box rationale, sample test, three-dictionary config, overrides, inline configs, multi-app, config search order, `extends`, `selectedConfiguration`, `reloadReactNative` caveat, `waitFor(...).withTimeout`. Removed: testID and locale advice, the claim about debug vs release behaviour, mocking and animation-disabling advice, failure-mode list, the claim that the map-based config replaced older layouts, "first match wins" wording, the Jest-by-default remark, and the old waitFor URL (404; replaced with the expect API page).
Method: documentation only; no commands were run.
