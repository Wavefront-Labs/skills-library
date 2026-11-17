---
id: computing-software.qa-testing-engineering.selenium.locator-strategies-and-finders
name: locator-strategies-and-finders
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [by-locators, xpath-locators, css-selectors, find-elements, selenium-webdriver]
level: practitioner
status: verified
description: "Choose Selenium locator strategies (id, name, CSS, XPath, link text) and finders (find_element vs find_elements, scoped searches) that are fast and robust."
sources:
  - https://www.selenium.dev/documentation/webdriver/elements/locators/
  - https://www.selenium.dev/documentation/webdriver/elements/finders/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locator strategies and finders

## The 8 strategies
| By | Example | Notes |
|---|---|---|
| `By.ID` | `"email"` | fastest, if ids are stable (not generated) |
| `By.NAME` | `"q"` | forms |
| `By.CSS_SELECTOR` | `"[data-test=submit]"` | preferred general-purpose |
| `By.XPATH` | `"//button[normalize-space()='Pay']"` | text matching, axes (ancestor) |
| `By.LINK_TEXT` / `PARTIAL_LINK_TEXT` | `"Sign out"` | anchors only |
| `By.TAG_NAME` | `"tr"` | inside scoped searches |
| `By.CLASS_NAME` | `"active"` | single class only, no spaces |

## Finders
```python
from selenium.webdriver.common.by import By
el = driver.find_element(By.CSS_SELECTOR, "[data-test=cart]")      # first match or NoSuchElementException
rows = driver.find_elements(By.CSS_SELECTOR, "table#orders tbody tr")  # [] when none (no exception, no wait unless implicit)
row = next(r for r in rows if "#1042" in r.text)
row.find_element(By.CSS_SELECTOR, "button.refund").click()          # scoped search from an element
active = driver.switch_to.active_element
```

## XPath patterns worth knowing
```
//label[normalize-space()='Email']/following-sibling::input
//tr[td[normalize-space()='#1042']]//button[.='Refund']
//*[contains(@class,'toast') and contains(.,'Saved')]
```
Avoid absolute paths (`/html/body/div[3]/...`) and index-heavy XPaths.

## Gotchas
- `find_elements` returning `[]` is not an error: assert on length explicitly.
- `By.CLASS_NAME, "btn primary"` is invalid (compound): chromedriver raised `InvalidSelectorException: Compound class names are not allowed`; use CSS `.btn.primary` (ran).
- XPath text matching is case-sensitive and whitespace-sensitive; use `normalize-space()` (ran: `'pay now'` matched 0 elements, `'Pay now'` matched 1).
- Locating with implicit waits set makes `find_elements` wait the full timeout when nothing matches (ran: `implicitly_wait(2)` made an empty `find_elements` take 2.0 s).

## Verify
In DevTools console: `$$('[data-test=submit]').length === 1` and `$x("//...")` for XPaths before committing.
