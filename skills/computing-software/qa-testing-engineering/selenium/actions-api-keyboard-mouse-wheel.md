---
id: computing-software.qa-testing-engineering.selenium.actions-api-keyboard-mouse-wheel
name: actions-api-keyboard-mouse-wheel
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [actions-api, selenium-actions, actionchains, drag-and-drop, keyboard-shortcuts]
level: practitioner
status: docs-checked
description: "Drive complex input with the Selenium Actions API: key chords, hover menus, drag and drop, click-and-hold, scroll wheel, pen input, and releasing actions."
sources:
  - https://www.selenium.dev/documentation/webdriver/actions_api/
  - https://www.selenium.dev/documentation/webdriver/actions_api/wheel/
  - https://www.selenium.dev/documentation/webdriver/actions_api/mouse/
  - https://www.w3.org/TR/webdriver2/#actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Actions API (keyboard, mouse, wheel)

**Goal:** perform low-level user input (hover, drag, key combinations, scroll) that simple `click`/`sendKeys` cannot. Based on W3C WebDriver Actions.

## Keyboard
```java
Keys mod = Platform.getCurrent().is(Platform.MAC) ? Keys.COMMAND : Keys.CONTROL;
new Actions(driver).keyDown(mod).sendKeys("a").keyUp(mod).sendKeys(Keys.DELETE).perform();
```
```python
from selenium.webdriver import ActionChains, Keys
ActionChains(driver).key_down(Keys.SHIFT).send_keys("abc").key_up(Keys.SHIFT).perform()
```

## Mouse
```java
WebElement menu = driver.findElement(By.id("account"));
new Actions(driver).moveToElement(menu).pause(Duration.ofMillis(300))
    .click(driver.findElement(By.linkText("Settings"))).perform();          // hover menu

new Actions(driver).dragAndDrop(source, target).perform();
new Actions(driver).clickAndHold(handle).moveByOffset(120, 0).release().perform();   // slider
new Actions(driver).contextClick(row).perform();
new Actions(driver).doubleClick(cell).perform();
```
Python: `ActionChains(driver).move_to_element(menu).click(item).perform()`, `drag_and_drop(src, dst)`, `click_and_hold().move_by_offset(120, 0).release()`.

## Wheel (Selenium 4.2+, Chromium)
```java
new Actions(driver).scrollToElement(footer).perform();
new Actions(driver).scrollFromOrigin(WheelInput.ScrollOrigin.fromElement(list), 0, 400).perform();
```
Python: `ActionChains(driver).scroll_to_element(el).scroll_by_amount(0, 400).perform()`.

## Release
`((RemoteWebDriver) driver).resetInputState()` (Java) / `ActionBuilder(driver).clear_actions()` (Python) releases pressed keys/buttons after a failed test.

## Gotchas
- `moveByOffset` moves from the current pointer position; `moveToElement(el, x, y)` moves to the element's in-view centre, then by the offset.
- Actions are not retried; wait for elements before building the chain.

## Verify
Hover menus, drag interactions and key chords pass on every browser in the matrix, with resets in teardown.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23, examples tracking Selenium 4.51). Confirmed: wheel actions are marked Selenium 4.2 and Chromium; `scrollToElement`, `scrollFromOrigin` and Python `scroll_to_element`/`scroll_by_amount` exist in the documented examples; `resetInputState()` (Java) and `ActionBuilder(driver).clear_actions()` (Python) are the documented release calls; the platform-dependent modifier key snippet matches the docs example; mouse offset semantics (element in-view centre, viewport, current pointer) match the mouse page. Removed: the HTML5 drag-and-drop browser-behaviour claim (not documented) and the 'since Selenium 4' wording on offsets.

Method: documentation only; no commands were run.
