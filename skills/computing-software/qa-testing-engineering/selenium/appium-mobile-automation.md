---
id: computing-software.qa-testing-engineering.selenium.appium-mobile-automation
name: appium-mobile-automation
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium, appium, selenium-framework, mobile-testing, uiautomator2, xcuitest, appium-inspector]
level: practitioner
status: docs-checked
description: "Automate native and hybrid mobile apps with Appium 2: drivers (UiAutomator2, XCUITest), capabilities, locator strategies, Appium Inspector and context switching."
sources:
  - https://appium.io/docs/en/latest/
  - https://appium.github.io/appium-inspector/latest/
  - https://github.com/appium/appium
  - https://github.com/appium/appium-uiautomator2-driver
  - https://github.com/appium/appium-xcuitest-driver
  - https://github.com/appium/python-client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Appium mobile automation

**Goal:** WebDriver-style automation for Android and iOS apps.

## Install (Appium 2)
```bash
npm i -g appium
appium driver install uiautomator2      # Android
appium driver install xcuitest          # iOS (macOS + Xcode)
appium driver doctor uiautomator2       # check environment (ANDROID_HOME or ANDROID_SDK_ROOT, JAVA_HOME)
appium                                  # server on :4723
```

## Session (Python)
```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "emulator-5554"
opts.app = "<APP_DIR>/app-debug.apk"
opts.auto_grant_permissions = True
driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Login").click()
```
iOS: `XCUITestOptions`, `appium:bundleId` or `appium:app` (.app/.ipa), `appium:udid` for real devices; real devices need WebDriverAgent signing and a provisioning profile (see the XCUITest device setup guide).

## Locators (best to worst)
Prefer `accessibility id` (Android content-desc via `UiSelector().description`; iOS name/accessibility identifier), `id` and the platform strategies (`-android uiautomator`, `-ios predicate string`, `-ios class chain`). The XCUITest driver rates accessibility id, id, name, class name and predicate string five stars, class chain four, and XPath two: XPath goes through the page source API and can be up to 10x slower. UiAutomator2 uses XPath 2 by default from driver 4.25.0 (`appium:enforceXPath1` restores XPath 1).
Inspect with **Appium Inspector** to find attributes.

## Hybrid apps and webviews
`driver.contexts` -> `['NATIVE_APP', 'WEBVIEW_com.shop']`; `driver.switch_to.context('WEBVIEW_com.shop')` then use web locators. UiAutomator2 names the context `WEBVIEW_` plus the app package (for example with `appium:autoWebview`).

## Gotchas
- `appium:noReset` and `appium:fullReset` control whether app data survives between sessions (the XCUITest driver documents them as mutually exclusive); choose deliberately.
- Capabilities need the `appium:` vendor prefix (or must be nested under `appium:options`), except standard W3C ones; the Python option classes add the prefix.

## Verify
A smoke test runs on one emulator and one real device (local or farm) using accessibility id locators only.

## Checked

Checked 2026-10-25 against the Appium docs source (appium/appium, pushed 2026-10-25), the UiAutomator2 and XCUITest driver docs and the Python client (all current trunk/default branches). Confirmed: `npm i -g appium`, `appium driver install uiautomator2|xcuitest`, `appium driver doctor`, default port 4723, ANDROID_HOME/ANDROID_SDK_ROOT and JAVA_HOME prerequisites, `UiAutomator2Options` and `XCUITestOptions`, the `auto_grant_permissions` option, `AppiumBy.ACCESSIBILITY_ID`, the locator strategy names and speed ratings, context names and `driver.contexts`/`switch_to.context`, `noReset`/`fullReset`, Appium Inspector. Removed as undocumented: the adb animation-scale commands, the webview-debugging remark and the explicit-wait advice; locator ranking rewritten to the documented speed ratings.

Method: documentation only; no commands were run.
