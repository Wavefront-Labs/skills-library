---
id: computing-software.qa-testing-engineering.selenium.shadow-dom-with-getshadowroot
name: shadow-dom-with-getshadowroot
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [shadow-root, shadow-dom, web-components, selenium-elements, getshadowroot]
level: practitioner
status: verified
description: "Locate elements inside shadow DOM with Selenium 4 shadow_root: nested roots, CSS-only search inside roots, and closed shadow roots on Chrome."
sources:
  - https://www.selenium.dev/documentation/webdriver/elements/finders/#shadow-dom
  - https://www.w3.org/TR/webdriver2/#get-element-shadow-root
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Goal:** interact with web components (design systems, Salesforce Lightning, Ionic) whose internals live in shadow roots.

```python
host = driver.find_element(By.CSS_SELECTOR, "my-date-picker")
host.shadow_root.find_element(By.CSS_SELECTOR, "button.next-month").click()

# nested components: one shadow_root per level
inner = (driver.find_element(By.CSS_SELECTOR, "custom-el").shadow_root
         .find_element(By.CSS_SELECTOR, "inner-el").shadow_root)
inner.find_element(By.CSS_SELECTOR, "a[href='/orders']").click()
```
Other bindings use `getShadowRoot()` (Java, JavaScript); only Python was run here.

## Rules
- Inside a shadow root use CSS selectors. On Chrome 156 `By.XPATH` and `By.TAG_NAME` both raised `InvalidArgumentException: invalid locator`, while `By.ID`, `By.CLASS_NAME` and CSS worked (all ran).
- Each nesting level needs another `shadow_root` access; write a helper that walks a list of host selectors.
- Wait for the host and the inner element; shadow content often renders after the host.

## Fallback
`driver.execute_script("return arguments[0].shadowRoot", host)` returned a `ShadowRoot` object for an open root (ran).

## Closed shadow roots
On Chrome 156 and chromedriver 156, `host.shadow_root` also worked on a `mode: 'closed'` root (the button inside was found and read), so closed roots are not necessarily out of reach through WebDriver. Other browsers were not tested; if a driver refuses, use a test-build flag to open the root or test the component in isolation.

## Gotchas
- `NoSuchShadowRootException` when the element has no shadow root (ran on a plain `div`).
- Slotted content (light DOM children projected into the shadow) is found from the normal DOM (`driver.find_element(By.ID, "slotted")` worked), not through the shadow root (`NoSuchElementException`); ran.

## Verify
Helper resolves nested roots with waits, and tests pass on every browser you support.
