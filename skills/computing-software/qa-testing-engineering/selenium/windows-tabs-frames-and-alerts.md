---
id: computing-software.qa-testing-engineering.selenium.windows-tabs-frames-and-alerts
name: windows-tabs-frames-and-alerts
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [switch-to-window, alerts-handling, iframes, window-handles, selenium-interactions]
level: practitioner
status: verified
description: "Handle browser windows, tabs, iframes and JavaScript alerts in Selenium (Python): window handles, new_window, switching frames, and accepting, dismissing and typing into alerts."
sources:
  - https://www.selenium.dev/documentation/webdriver/interactions/windows/
  - https://www.selenium.dev/documentation/webdriver/interactions/frames/
  - https://www.selenium.dev/documentation/webdriver/interactions/alerts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows, tabs, frames and alerts (Selenium)

Examples are Python (ran on Selenium 4.51 with Chrome 156); Java and other bindings use equivalent methods.

## Windows and tabs
```python
original = driver.current_window_handle
driver.find_element(By.LINK_TEXT, "Terms").click()            # target=_blank opens a new tab
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
new = next(h for h in driver.window_handles if h != original)
driver.switch_to.window(new)
driver.close()                       # closes current tab only
driver.switch_to.window(original)    # must switch back
driver.switch_to.new_window("tab")   # Selenium 4: open and switch
```
After `driver.close()` without switching back, the next command (`driver.title`) raised `NoSuchWindowException: target window already closed`.

## Frames
```python
WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#payment")))
driver.find_element(By.NAME, "cardnumber").send_keys("4242424242424242")
driver.switch_to.default_content()   # back to top-level document
```
Nested: `switch_to.frame(outer)` then `switch_to.frame(inner)`; `switch_to.parent_frame()` goes up one level and `default_content()` goes to the top (ran with two nested iframes). Switch by WebElement, name/id, or index (index is fragile); WebElement, name and index all worked. Finding an element inside an iframe without switching raised `NoSuchElementException`.

## Alerts (JS alert/confirm/prompt)
```python
driver.find_element(By.ID, "delete").click()
alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
assert alert.text == "Delete order?"
alert.accept()           # or dismiss(); prompt: alert.send_keys("reason") then accept()
```
Ran for alert, confirm (dismiss gave `false`) and prompt (typed text returned). A click while an alert was open raised `UnexpectedAlertPresentException`. The default `unhandledPromptBehavior` capability was `dismiss and notify`; setting `options.unhandled_prompt_behavior = "accept"` reported `accept` back and the same click raised nothing.

## Gotchas
- Elements found in one frame/window are stale after switching away.
- Custom HTML modals are not alerts; locate them as elements.

## Verify
Tests always return to the original window/default content in teardown, and window/frame switches use explicit waits.
