---
id: computing-software.qa-testing-engineering.selenium.relative-locators
name: relative-locators
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [relative-locators, selenium-locators, locate-with, webdriver, selenium-4]
level: practitioner
status: verified
description: "Use Selenium 4 relative locators (above, below, to_left_of, to_right_of, near) in Python, how they rank matches, and when they are fragile."
sources:
  - https://www.selenium.dev/documentation/webdriver/elements/locators/#relative-locators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Goal:** locate elements by visual position relative to a known element when no good attribute exists.

```python
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By

email = driver.find_element(locate_with(By.TAG_NAME, "input").above({By.ID: "password"}))
cancel = driver.find_element(locate_with(By.TAG_NAME, "button").to_left_of({By.ID: "submit"}))
help_link = driver.find_element(locate_with(By.TAG_NAME, "a").near({By.ID: "postcode"}, 100))
```
The anchor can be a locator dict as above or a `WebElement` (`.above(driver.find_element(...))`); both ran. Chains work: `locate_with(By.TAG_NAME, "input").below({By.ID: "email"}).above({By.ID: "postcode"})` returned only the input between them. Other bindings have equivalents (`RelativeLocator.with` in Java, `locateWith` in JavaScript); only Python was run here.

## How it works
`find_elements` returns every match, nearest first: on a test page `above({By.ID: "postcode"})` returned `password` before `email`, and `near` returned the closer link first.

## When to use
- Legacy apps with generated ids and no labels or test ids.
- Form fields identified only by a nearby visual label.

## When not to
- Responsive layouts: the relation depends on rendered positions, so check it at each viewport size you test.
- Elements not yet rendered or offscreen: wait for visibility first.
- Prefer accessible attributes (label `for`, aria-label) or adding `data-testid`.

## Gotchas
- `near` default distance is 50 px (`near(element_or_locator, distance: int = 50)` in the Python binding); on the test page two links just below the anchor matched at the default, while one more than 200 px away only matched with `near(..., 300)`.
- Overlapping elements and transforms (CSS animations) confuse position checks.

## Verify
Locator returns the intended element at every viewport size you test, or is replaced by an attribute-based locator.
