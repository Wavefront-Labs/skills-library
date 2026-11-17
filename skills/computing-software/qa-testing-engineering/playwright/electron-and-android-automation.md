---
id: computing-software.qa-testing-engineering.playwright.electron-and-android-automation
name: electron-and-android-automation
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright-electron, playwright-android, electron-testing, android-webview, desktop-app-testing]
level: practitioner
status: docs-checked
description: "Automate Electron apps and Android Chrome/WebView with Playwright: _electron.launch, main-process evaluate, adb device connection, and their experimental limits."
sources:
  - https://playwright.dev/docs/api/class-electron
  - https://playwright.dev/docs/api/class-android
  - https://playwright.dev/docs/ci
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android and Electron automation (Playwright)

**Goal:** reuse Playwright skills for Electron desktop apps and Chrome/WebView on Android devices. Both APIs are marked experimental.

## Electron
```ts
import { test, expect } from '@playwright/test';
import { _electron as electron } from 'playwright';

test('opens settings', async () => {
  const app = await electron.launch({ args: ['.'], env: { ...process.env, NODE_ENV: 'test' } });
  const appPath = await app.evaluate(async ({ app }) => app.getAppPath());   // runs in main process
  const window = await app.firstWindow();
  await window.getByRole('button', { name: 'Settings' }).click();
  await expect(window.getByRole('heading', { name: 'Settings' })).toBeVisible();
  await window.screenshot({ path: 'settings.png' });
  await app.close();
});
```
- `executablePath` to launch a packaged build instead of the source folder.
- `app.windows()` and `app.on('window')` for multi-window apps.
- Supported Electron versions: v21 and newer.
- If launch times out, make sure the `nodeCliInspect` fuse (`FuseV1Options.EnableNodeCliInspectArguments`) is not set to `false`.

## Android
```ts
import { _android as android } from 'playwright';
const [device] = await android.devices();          // needs a running, authenticated ADB daemon
await device.shell('am force-stop com.android.chrome');
const context = await device.launchBrowser();       // Chrome on device
const page = await context.newPage();
await page.goto('https://example.test');
// WebView of an app, selected by package name:
const webview = await device.webView({ pkg: 'com.example.app' });
const wvPage = await webview.page();
```
Requirements per the docs: an Android device or AVD emulator, the ADB daemon running and authenticated (`adb devices`), Chrome 105 or newer on the device, and "Enable command line on non-rooted devices" enabled in `chrome://flags`. Raw USB is not supported, so ADB is needed; the device must be awake to produce screenshots (enable "Stay awake").

## Gotchas
- Both APIs are marked experimental in the docs; check the release notes when upgrading Playwright.
- The Android docs note that not all tests were run against devices, so not everything works.

## Verify
An Electron smoke test passes in CI (on Linux agents headed runs need Xvfb, e.g. `xvfb-run` before the command), and an Android WebView test runs against an emulator.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: both APIs being experimental, the _electron namespace with launch, firstWindow, windows, the window event and executablePath, evaluate running in the main Electron process, supported Electron versions (v21 and newer) and the nodeCliInspect fuse note, the _android namespace with devices, shell, launchBrowser and webView with pkg, the Android requirements (ADB, Chrome 105 or newer, chrome://flags setting, device awake), and Xvfb for headed Linux runs. Corrected: Electron versions (was v12.2+, v13.4+, v14+) and minimum Chrome (was 87+). Removed: the Android 9 requirement, the Appium/Espresso remark, the dialog-mock snippet and the nodeIntegration claim.

Method: documentation only; no commands were run.
