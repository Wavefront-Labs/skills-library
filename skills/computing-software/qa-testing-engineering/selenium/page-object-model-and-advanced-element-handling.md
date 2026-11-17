---
id: computing-software.qa-testing-engineering.selenium.page-object-model-and-advanced-element-handling
name: page-object-model-and-advanced-element-handling
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium, page-object-model, pom, data-driven-testing, iframe, switch-to-frame, shadow-dom, file-upload, file-download, javascriptexecutor, actions-class, drag-and-drop, stale-element-reference, element-interaction, python, java]
level: advanced
status: verified
description: "Structure Selenium suites with a maintainable Page Object Model, parameterize them for data-driven runs, and handle iframes, shadow DOM, file upload/download, and drag-and-drop correctly."
sources: ["https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selenium: Page Object Model and the elements that don't behave

**Goal:** a suite structured so a UI change requires editing one file, not every
test that touches that screen — plus the handling for iframes, shadow DOM, file
I/O, and drag-and-drop that a basic `find_element`/`click` doesn't cover.

## 1. Page Object Model, done right
One class per page/component; locators and low-level interactions live there,
tests call only behavior-named methods:
```python
class LoginPage:
    def __init__(self, driver): self.driver = driver
    def login(self, user, pwd):
        self.driver.find_element(By.ID, 'user').send_keys(user)
        self.driver.find_element(By.ID, 'pass').send_keys(pwd)
        self.driver.find_element(By.ID, 'submit').click()
        return DashboardPage(self.driver)
```
Return the **next page object** from an action that navigates — this chains
naturally and makes an invalid transition (e.g., calling a dashboard method
before login redirected) a type error, not a runtime surprise. Keep assertions
out of page objects; they describe the page's capabilities, not the test's
expectations — assertions belong in the test.

## 2. Data-driven tests over copy-pasted test methods
Parameterize instead of duplicating a test per input set:
```python
@pytest.mark.parametrize('user,pwd,expected', [('a@x.com','p1','Dashboard'),
                                                 ('bad@x.com','wrong','Invalid credentials')])
def test_login(user, pwd, expected): ...
```
This turns "10 near-identical test methods" into one
method and a data table — the common failure mode it prevents is a bug fixed in
one copy and left broken in the other nine.

## 3. Iframes
Elements inside an `<iframe>` are invisible to `find_element` until you switch
context:
```python
driver.switch_to.frame('billing-iframe')   # by name/id, index, or WebElement
driver.find_element(By.ID, 'card-number').send_keys('4242...')
driver.switch_to.default_content()          # back out — easy to forget, breaks every later call
```
Nested iframes need a `switch_to.frame` per level in, and `default_content()`
returns to the top, not one level up; `driver.switch_to.parent_frame()` goes up exactly one level (ran with two nested iframes).

## 4. Shadow DOM
Standard locators can't pierce a shadow root. Selenium 4 exposes
`element.shadow_root` once you have the host element:
```python
host = driver.find_element(By.CSS_SELECTOR, 'my-widget')
shadow = host.shadow_root
shadow.find_element(By.CSS_SELECTOR, '.inner-button').click()
```
Closed shadow roots (`mode: 'closed'`) were reachable too: on Chrome 156 `host.shadow_root.find_element(...)` found a button inside a `mode: 'closed'` root, so do not assume they need a test-build flag (other browsers were not tested). Inside a shadow root use CSS selectors: `By.XPATH` and `By.TAG_NAME` raised `InvalidArgumentException: invalid locator` (ran).

## 5. File upload, download, and drag-and-drop
- **Upload**: don't click a styled button and hunt for a native OS file dialog —
  Selenium can't interact with OS-native dialogs. Instead, `send_keys()` the
  absolute file path directly to the (often visually hidden) `<input type=file>`
  element.
- **Download**: configure the browser profile to auto-save to a known directory
  with no "save as" prompt (Chrome: `prefs: {'download.default_directory': path,
  'download.prompt_for_download': False}`), then poll the filesystem for the file
  rather than trying to observe the download through the DOM.
- **Drag-and-drop**: `ActionChains(driver).drag_and_drop(source, target).perform()`
  fired a native HTML5 `drop` (ran) and also delivered `pointerdown`, `pointermove` and `pointerup` to a plain pointer-event listener (ran on Chrome 156). Some drag libraries need more than that; if a `drag_and_drop` call "succeeds" (no exception) but nothing moves, simulate
  the actual pointer sequence instead:
  `click_and_hold(source).move_to_element(target).release().perform()`, or dispatch
  synthetic `pointerdown`/`pointermove`/`pointerup` via `JavascriptExecutor` matching
  what the library listens for.

## Unconfirmed / notes
Drag library compatibility is app-specific (only two toy pages were tried); verify directly against the target app.

## Verify
- [ ] Page objects return the next page object on navigating actions; no assertions inside them.
- [ ] Repeated test variants collapsed into one parameterized test + data table.
- [ ] `switch_to.default_content()` called after every completed iframe interaction.
- [ ] File upload sends the path to the input element directly, never via an OS dialog.
- [ ] Drag-and-drop verified with a real pointer-event simulation if `ActionChains` silently no-ops.
