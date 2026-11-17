---
id: computing-software.software-engineering.tauri.tauri-webdriver-testing
name: tauri-webdriver-testing
category: computing-software
field: software-engineering
product: tauri
tags: [webdriver-testing, tauri, e2e, webdriverio]
level: practitioner
status: docs-checked
description: "Set up WebDriver end-to-end tests for Tauri with the WebdriverIO tauri service, or drive tauri-driver directly on Windows and Linux."
sources:
  - "https://v2.tauri.app/develop/tests/webdriver/"
  - "https://v2.tauri.app/develop/tests/webdriver/manual-setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebDriver testing for Tauri

Goal: run end-to-end tests against a Tauri app. The recommended route is WebdriverIO with `@wdio/tauri-service` (Windows, Linux, macOS). It offers `browser.tauri.execute()`, command (IPC) mocking, frontend and backend log capture, and multiremote.

## Recommended: WebdriverIO service

Scaffold with `npm create wdio@latest ./`, pick **Desktop Testing**, then **Tauri**. Minimal config:

```typescript
export const config: WebdriverIO.Config = {
  services: [
    ['tauri', {
      appBinaryPath: './src-tauri/target/release/my-tauri-app',
      driverProvider: 'embedded',
    }],
  ],
};
```

Driver providers:

- `embedded` (default): an embedded WebDriver server runs inside your app, no external driver needed; this is how macOS is supported.
- `external`: native WebDriver through `tauri-driver` on Windows and Linux.
- `crabnebula`: CrabNebula's cross-platform fork of `tauri-driver` (a paid API key is required for macOS).

Two optional Tauri plugins:

- `tauri-plugin-wdio-webdriver`: runs the embedded server; required for `embedded`, skippable for `external` or `crabnebula`.
- `tauri-plugin-wdio`: enables backend access (`browser.tauri.execute()`, IPC mocking, log capture).

A renderer-only browser mode runs your frontend in plain Chrome against a Vite dev server, with no Tauri binary, driver or plugin, intercepting `invoke()` calls.

## Driving tauri-driver directly

For non-Node setups, Selenium, or custom harnesses. Only Windows and Linux are supported (macOS has no WKWebView driver tool). iOS and Android work via Appium 2, not streamlined.

1. Install: `cargo install tauri-driver --locked`.
2. Linux: needs `WebKitWebDriver`; check with `which WebKitWebDriver`. Debian-based distributions package it as `webkit2gtk-driver`.
3. Windows: use the Microsoft Edge Driver matching your Edge version; a mismatch can make the suite hang while connecting. Download with msedgedriver-tool:
   `cargo install --git https://github.com/chippers/msedgedriver-tool` then `& "$HOME/.cargo/bin/msedgedriver-tool.exe"`.
   `tauri-driver` finds `msedgedriver.exe` on `$PATH`, or use its `--native-driver` option.

A finished minimal example is at https://github.com/tauri-apps/webdriver-example.

## Checked

Checked 2026-11-08 against the Tauri v2 WebDriver overview and manual setup pages: @wdio/tauri-service features and platforms, minimal config, the three driver providers, the two plugins, browser mode, tauri-driver install, WebKitWebDriver and Edge Driver requirements and the example repository. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
