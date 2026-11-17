---
id: computing-software.qa-testing-engineering.selenium.browser-options-chrome-edge-firefox
name: browser-options-chrome-edge-firefox
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [chromeoptions, browser-options, headless, firefox-options, selenium-drivers]
level: practitioner
status: docs-checked
description: "Configure Selenium browser options: headless=new, window size, prefs for downloads, arguments, page load strategy, Firefox profiles, and Edge options in Java and Python."
sources:
  - https://www.selenium.dev/documentation/webdriver/browsers/chrome/
  - https://www.selenium.dev/documentation/webdriver/browsers/edge/
  - https://www.selenium.dev/documentation/webdriver/browsers/firefox/
  - https://www.selenium.dev/documentation/webdriver/drivers/options/
  - https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chrome/Edge/Firefox options (Selenium)

## Chrome / Edge (Java)
```java
ChromeOptions options = new ChromeOptions();
options.addArguments("--headless=new", "--start-maximized");
options.setPageLoadStrategy(PageLoadStrategy.EAGER);          // return at DOMContentLoaded
options.setExperimentalOption("excludeSwitches", List.of("disable-popup-blocking"));   // drop a chromedriver default argument
options.setAcceptInsecureCerts(true);                          // self-signed test envs
options.setBrowserVersion("stable");                           // Selenium Manager fetches it
WebDriver driver = new ChromeDriver(options);
```
Edge: `EdgeOptions` with the same Chromium arguments.

## Python
```python
from selenium import webdriver
opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")
opts.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
opts.page_load_strategy = "eager"
driver = webdriver.Chrome(options=opts)
```

## Firefox
```java
FirefoxOptions ff = new FirefoxOptions();
ff.addArguments("-headless");
```

## Common arguments
The Selenium docs list `--start-maximized`, `--headless=new` and `--user-data-dir=...` as commonly used Chrome and Edge arguments, and `-headless` and `-profile <path>` for Firefox. `excludeSwitches` removes chromedriver's own default arguments (the docs' example turns the popup blocker back on). Download folders are browser settings; on a remote Grid they live on the node, so use the Grid's managed downloads (`--enable-managed-downloads true` and the `se:downloadsEnabled` capability).

## Page load strategy
`normal` (default; document readiness `complete`, waits for all resources), `eager` (document readiness `interactive`: DOM access is ready but images may still be loading), `none` (does not block WebDriver at all). The strategy applies to the whole session; use `eager` or `none` only with explicit waits.

## Gotchas
- Use `--headless=new` as the Selenium docs show for Chrome and Edge; set the window size explicitly because responsive layouts depend on it.

## Verify
Headless and headed runs render the same layout at the configured window size.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23). Confirmed: `--headless=new`, `--start-maximized` and `--user-data-dir` as commonly used Chrome/Edge arguments; Firefox `-headless`; `excludeSwitches` semantics; `setBrowserVersion("stable")`; `acceptInsecureCerts`; the page load strategy table (normal/complete default, eager/interactive, none); Grid `--enable-managed-downloads true` and `se:downloadsEnabled`. Removed as undocumented: Chrome prefs for downloads and notifications, Firefox download preferences, `--lang`, `--window-size`, `--disable-gpu`, `--no-sandbox`, `--disable-dev-shm-usage`, `--incognito`, `--force-device-scale-factor`, the Chrome 109 headless history and the 800x600 default window size.

Method: documentation only; no commands were run.
