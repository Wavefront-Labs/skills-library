---
id: computing-software.qa-testing-engineering.selenium.safari-and-ie-mode-drivers
name: safari-and-ie-mode-drivers
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [safaridriver, ie-mode, edge-ie-mode, safari-technology-preview, legacy-browsers]
level: practitioner
status: gated
description: "Run Selenium on Safari (safaridriver enable, limits, one session per machine) and on Edge IE mode for legacy apps with InternetExplorerOptions."
sources:
  - https://www.selenium.dev/documentation/webdriver/browsers/safari/
  - https://www.selenium.dev/documentation/webdriver/browsers/internet_explorer/
  - https://www.selenium.dev/documentation/ie_driver_server/
  - https://developer.apple.com/documentation/webkit/about_webdriver_for_safari
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safari and IE mode drivers

## Safari
```bash
safaridriver --enable      # once per macOS machine (admin); or Safari > Develop > Allow Remote Automation
```
```python
options = webdriver.SafariOptions()
# options.use_technology_preview = True   # Safari Technology Preview
driver = webdriver.Safari(options=options)
```
Constraints:
- macOS only; no headless mode (gated: unconfirmed, source is paywalled or blocked). Apple's developer documentation could not be read in this review.
- One session at a time per machine (gated: unconfirmed, source is paywalled or blocked). Apple's developer documentation could not be read in this review.
- Safari-specific capabilities are listed on Apple's page "About WebDriver for Safari"; check it for feature gaps.
- The Selenium docs point iOS Safari automation to Appium, not safaridriver.

## Edge IE mode (legacy IE11 apps)
Selenium drives Edge in IE Compatibility mode via IEDriverServer:
```python
from selenium.webdriver.ie.options import Options as IeOptions
opts = IeOptions()
opts.attach_to_edge_chrome = True
opts.edge_executable_path = EDGE_PATH   # full path to msedge.exe on the Windows host
driver = webdriver.Ie(options=opts)
```
Requirements from the Selenium docs: the 32-bit IEDriverServer is recommended, Protected Mode must be the same for every zone, Enhanced Protected Mode must be disabled, and browser zoom must be 100% (`ignoreZoomSetting` relaxes the zoom check). Standalone Internet Explorer has not been supported by Selenium since June 2022; only Edge in IE Compatibility mode is.

## Strategy
Run the bulk of the suite on Chromium/Firefox; a targeted Safari smoke set on real macOS (or cloud); IE mode only for apps contractually needing it.

## Gotchas
- IE mode: the `ignoreProtectedModeSettings` option bypasses the Protected Mode check; prefer fixing the zone settings.

## Verify
A Safari smoke job runs serially on a macOS runner; the IE mode job starts Edge in IE Compatibility mode.

## Checked

Checked 2026-10-25 against the Selenium documentation source (pushed 2026-10-23) and the Selenium Python IE options source. Confirmed: `safaridriver --enable`, Safari Technology Preview, iOS via Appium, `attach_to_edge_chrome` (`ie.edgechromium`) and `edge_executable_path` (`ie.edgepath`), 32-bit driver recommendation, Protected Mode and 100% zoom requirements, Selenium ending support for standalone IE in June 2022. Not confirmed: Safari's one-session and no-headless limits (Apple's page content could not be read). Removed: the Safari timing and glass-pane remarks, the Windows-only and no-parallel IE remarks, and the `document.documentMode` check.

Method: documentation only; no commands were run.
