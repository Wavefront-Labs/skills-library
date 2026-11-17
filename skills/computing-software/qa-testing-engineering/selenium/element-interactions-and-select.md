---
id: computing-software.qa-testing-engineering.selenium.element-interactions-and-select
name: element-interactions-and-select
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [select-class, send-keys, element-interactions, clear, submit]
level: practitioner
status: verified
description: "Interact with elements in Selenium: click, send_keys with special keys, clear, the Select class for dropdowns, checkboxes and file inputs, plus interactability errors."
sources:
  - https://www.selenium.dev/documentation/webdriver/elements/interactions/
  - https://www.selenium.dev/documentation/webdriver/support_features/select_lists/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Element interactions (click, send_keys, clear, Select)

## Basic commands
```python
from selenium.webdriver.common.keys import Keys
el = driver.find_element(By.NAME, "q")
el.clear()
el.send_keys("selenium", Keys.ENTER)
el.send_keys(Keys.CONTROL, "a")   # select all (Keys.COMMAND on macOS)
driver.find_element(By.ID, "agree").click()
```
The Selenium docs list only 5 basic element commands: click, send keys, clear, submit (form elements only) and select. Everything else is the Actions API.

## Select lists
```python
from selenium.webdriver.support.select import Select
sel = Select(driver.find_element(By.ID, "country"))
sel.select_by_visible_text("New Zealand")
sel.select_by_value("NZ")
sel.select_by_index(2)
assert sel.first_selected_option.text == "New Zealand"
[o.text for o in sel.options]
if sel.is_multiple: sel.deselect_all()
```
`Select` only works on native `<select>`. Selecting a disabled option raises `NotImplementedError: You may not select a disabled option`, and `deselect_all()` on a single select raises `NotImplementedError` (ran). `Select.is_multiple` is falsy (`None`) for a single select, not necessarily `False`. Custom dropdowns: click to open, click option by text.

## Checkboxes and radios
```python
cb = driver.find_element(By.ID, "newsletter")
if not cb.is_selected(): cb.click()
```

## File upload
```python
driver.find_element(By.CSS_SELECTOR, "input[type=file]").send_keys(str(Path("fixtures/a.pdf").resolve()))
```
Absolute path required (a relative path raised `InvalidArgumentException: path is not absolute`; ran). Hidden `display:none` file inputs still accepted the path. On Remote/Grid, the Selenium docs say to set a `LocalFileDetector` to upload from the client machine (not run here: no Grid).

## Errors
- `ElementNotInteractableException`: hidden/zero size, or `send_keys` to a disabled input; wait for visibility or interact with the visible proxy element (ran).
- `ElementClickInterceptedException`: overlay at the click point; wait for it to disappear (ran).
- `InvalidElementStateException` on `clear()`: element is readonly/disabled (ran on both).
- `click()` on a disabled button raised nothing and did nothing.

## Gotchas
- `clear()` fires `focus`, `change` and `blur` but no `input` event (ran), so frameworks that listen to `input` (React `onChange`) can miss it; use `Keys.CONTROL, "a"` then `Keys.DELETE` instead, which does fire `keydown` and `input`.
- `send_keys` appends; clear first when replacing values.

## Verify
Assert on resulting state (`get_property("value")`, `is_selected()`, displayed confirmation), not on lack of exceptions.
