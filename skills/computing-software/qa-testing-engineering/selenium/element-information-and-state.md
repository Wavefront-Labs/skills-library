---
id: computing-software.qa-testing-engineering.selenium.element-information-and-state
name: element-information-and-state
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [element-information, is-displayed, get-attribute, get-dom-property, element-rect]
level: practitioner
status: verified
description: "Read element state in Selenium correctly: is_displayed, is_enabled, is_selected, text, get_attribute vs get_dom_property vs get_dom_attribute, CSS values and rect."
sources:
  - https://www.selenium.dev/documentation/webdriver/elements/information/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Element information

```python
el = driver.find_element(By.ID, "email")
el.is_displayed(); el.is_enabled(); el.is_selected()
el.tag_name                          # "input"
el.text                              # rendered, visible text only
el.rect                              # {'x','y','width','height'}
el.value_of_css_property("color")    # "rgba(255, 0, 0, 1)"
el.accessible_name; el.aria_role     # computed a11y name/role (ran: 'textbox', 'button')
```

## Attribute vs property
| Method | Returns |
|---|---|
| `get_dom_attribute("value")` | the HTML attribute as written in markup (initial value) |
| `get_property("value")` | live JS property (current value after typing) |
| `get_attribute("value")` | legacy hybrid: property if present else attribute (uses an injected atom) |
The Python binding names the property getter `get_property`; there is no `get_dom_property` on `WebElement` in Selenium 4.51 (`AttributeError`; that name belongs to the Java binding). Use `get_property("value")` for the current input value, `get_dom_attribute("href")` for the literal href (`/page2.html`), `get_property("href")` for the resolved absolute URL (`http://127.0.0.1:PORT/page2.html`). `get_property("checked")` returns a boolean; `get_dom_attribute("checked")` returns the string `'true'`.

## text pitfalls
- `.text` is empty for hidden elements and does not include input values.
- Whitespace is normalised the way the browser renders it; compare with `.strip()`.
- `textContent` for hidden text: `el.get_property("textContent")` (ran: `.text` was `''`, `textContent` was `'hidden text'`).

## is_displayed
Implemented with a JS atom approximating visibility. On Chrome 156 an element with `opacity:0`, `visibility:hidden` or a 0x0 size reported `False`. It does not know about elements covered by overlays: a covered button is still displayed, and clicking it raises `ElementClickInterceptedException` (ran).

## Gotchas
- Reading information doesn't wait; pair with `WebDriverWait` (`visibility_of_element_located`, `text_to_be_present_in_element`).
- Colour values come back in `rgba(...)` form; normalise with `Color.from_string(...)` (`selenium.webdriver.support.color`).

## Verify
After typing into a field, `get_property("value")` reflects the new text (`origX`) while `get_dom_attribute("value")` shows the original (`orig`); ran.
