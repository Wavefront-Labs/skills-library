---
id: computing-software.qa-testing-engineering.selenium.webdriver-tests-with-explicit-waits
name: webdriver-tests-with-explicit-waits
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium, selenium-webdriver, webdriver, selenium-manager, selenium-grid, explicit-wait, webdriverwait, expected-conditions, implicit-wait, locators, css-selector, xpath, stale-element, cross-browser, headless, chrome, firefox, edge, remotewebdriver, page-object, browser-automation, e2e-testing, python, java]
level: practitioner
status: gated
description: "Write stable Selenium 4 WebDriver tests: Selenium Manager drivers, robust locators, explicit waits (never mixed with implicit), page objects, headless and Grid cross-browser runs."
sources: ["https://www.selenium.dev/documentation/webdriver/", "https://www.selenium.dev/documentation/grid/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selenium WebDriver tests that don't flake

**Goal:** browser tests that pass for the right reason every run, locally and on a
Grid, across Chrome, Firefox and Edge. Examples are Python (`pip install selenium`);
the Java/JS/C# APIs map one-to-one.

## 1. Driver setup (Selenium 4.6+)
You no longer download chromedriver by hand: **Selenium Manager** (bundled) resolves
a matching driver — and on recent versions a browser too — on first use.
```python
from selenium import webdriver
opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")          # the modern headless mode
opts.add_argument("--window-size=1366,900")  # headless default is 780x580 (ran on Chrome 156); layout changes!
driver = webdriver.Chrome(options=opts)
try:
    driver.get("https://example.test/login")
finally:
    driver.quit()                            # quit(), not close(): close() leaves the driver process
```
Gotcha: behind a corporate proxy or offline CI, Selenium Manager can't download;
pre-install the browser/driver in the image or point Selenium Manager at a mirror (`SE_DRIVER_MIRROR_URL`, env form of `--driver-mirror-url`), a cache (`SE_CACHE_PATH`) or offline mode (`SE_OFFLINE=true`, which logged "Unable to discover proper chromedriver version in offline mode" when the cache was empty). The env names follow the table in the Selenium Manager docs and `selenium-manager --help` (4.51).

## 2. Locators, in order of preference
1. A dedicated test attribute: `By.CSS_SELECTOR, "[data-testid='submit']"` — ask devs to add them.
2. `By.ID` / `By.NAME` if stable (not auto-generated like `ember1234`).
3. Short CSS on semantic structure: `form#login button[type=submit]`.
4. XPath only for text or upward traversal: `//button[normalize-space()='Sign in']`.
Avoid absolute XPath (`/html/body/div[3]/...`) and styling classes — they break on any redesign.

## 3. Waits: the single biggest source of flakiness
- Use **explicit waits** for every condition the page reaches asynchronously:
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='submit']"))).click()
wait.until(EC.url_contains("/dashboard"))
wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".spinner")))
```
- **Never mix implicit and explicit waits.** The docs say: "Do not mix implicit and explicit waits. Doing so can cause unpredictable wait times." Ran: with `implicitly_wait(5)` a 1 s `WebDriverWait` for a missing element took 5.0 s. Leave `implicitly_wait` at 0 and use explicit waits only.
- **No `time.sleep()`** except while debugging. It is either too short (flaky) or too long (slow).
- Wait for the *outcome* the user sees (text appears, row count changes), not just
  for an element to exist — "present in DOM" is not "rendered and populated".

## 4. Common exceptions and their real cause
| Exception | Usual cause | Fix |
|---|---|---|
| `StaleElementReferenceException` | DOM re-rendered after you found the element (React/Vue re-render) | Re-find inside the wait; don't cache elements across actions |
| `ElementClickInterceptedException` | Overlay, cookie banner or sticky header covers it | Wait for overlay invisible; dismiss banner in setup; scroll into view |
| `NoSuchElementException` | Wrong locator, or inside an `iframe` / shadow root | `driver.switch_to.frame(...)`; `element.shadow_root` |
| `TimeoutException` | Condition never met — read the screenshot | Save `driver.save_screenshot()` + `page_source` on failure |

## 5. Page Object Model
Put locators and actions in one class per page/component; tests read as user intent:
```python
class LoginPage:
    USER = (By.ID, "username"); PASS = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "[data-testid='submit']")
    def __init__(self, driver): self.d, self.w = driver, WebDriverWait(driver, 10)
    def login(self, u, p):
        self.w.until(EC.visibility_of_element_located(self.USER)).send_keys(u)
        self.d.find_element(*self.PASS).send_keys(p)
        self.d.find_element(*self.SUBMIT).click()
```
Assertions stay in tests, not page objects.

## 6. Cross-browser with Selenium Grid
Quick local Grid via Docker:
```bash
docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:latest
```
```python
driver = webdriver.Remote("http://localhost:4444", options=webdriver.FirefoxOptions())
```
(gated: unconfirmed, source is paywalled or blocked) Docker and a Grid are not available here, so the image names, port, `--shm-size` guidance and Grid UI path were not run. Note the example pairs a Chrome image with Firefox options; use `selenium/standalone-firefox` for that.
`--shm-size=2g` matters: Chrome crashes with the default 64 MB `/dev/shm`. For multi-browser
use `docker compose` with a hub plus `node-chrome`/`node-firefox`/`node-edge` images;
the Grid UI at `:4444/ui` shows sessions. Pin image tags in CI rather than `latest`.
Run in parallel with `pytest -n 4` (pytest-xdist) — each worker needs its own driver.

## Notes
The Python waits, locator and exception examples above ran on Selenium 4.51 with Chrome 156 (each exception in the table was reproduced: stale after `refresh()`, click intercepted by an overlay, no such element in an iframe, wait timeout). Selenium Manager's env-var names have changed across 4.x minors; check `selenium-manager --help` for your version.

## Verify
- [ ] `implicitly_wait` is not set anywhere; no `sleep` in committed tests.
- [ ] Every locator is a test-id, ID or short CSS — no absolute XPath.
- [ ] Failures save a screenshot and page source.
- [ ] Suite passes 10 consecutive runs headless (`for i in $(seq 10); do pytest -q || break; done`).
- [ ] Same suite passes against Chrome and Firefox on the Grid.
- [ ] `driver.quit()` runs in a fixture finaliser even when a test fails.
