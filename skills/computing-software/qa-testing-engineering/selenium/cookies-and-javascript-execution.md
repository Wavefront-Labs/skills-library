---
id: computing-software.qa-testing-engineering.selenium.cookies-and-javascript-execution
name: cookies-and-javascript-execution
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium-cookies, execute-script, execute-async-script, add-cookie, javascript-executor]
level: practitioner
status: verified
description: "Manage cookies (add, get, delete, domain rules) and run JavaScript in Selenium with execute_script and execute_async_script, knowing when JS shortcuts invalidate a test."
sources:
  - https://www.selenium.dev/documentation/webdriver/interactions/cookies/
  - https://www.selenium.dev/documentation/webdriver/interactions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cookies and JavaScript execution

## Cookies
```python
driver.get("https://app.test/404")                 # must be on the cookie's domain first
driver.add_cookie({"name": "session", "value": token, "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"})
driver.refresh()
driver.get_cookie("session"); driver.get_cookies()
driver.delete_cookie("consent"); driver.delete_all_cookies()
```
- You can only add cookies for the current domain; navigate to a cheap page (404, static asset) first. Adding one from a `data:` page or with a mismatched `domain` raises `InvalidCookieDomainException` (ran on Chrome 156 and chromedriver 156).
- `secure: True` cookies were accepted on a plain `http://127.0.0.1` page.
- Login by injecting a session cookie obtained via API speeds up suites: one UI login test, all others via cookie.

## JavaScript
```python
driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", el)
title = driver.execute_script("return document.title")
driver.execute_script("window.localStorage.setItem('flag', arguments[0])", "on")
# async: last argument is the callback
result = driver.execute_async_script("""
  const done = arguments[arguments.length - 1];
  fetch('/api/health').then(r => r.json()).then(done);
""")
```
`set_script_timeout(30)` governs async scripts. Returned values are converted: elements -> WebElement, arrays -> lists, objects -> dicts.

## When JS is legitimate vs cheating
- OK: reading app state, setting up storage, scrolling, triggering hard-to-reach diagnostics.
- Avoid: `arguments[0].click()` or setting `.value` to bypass a click/typing that fails; users can't do that, so the test stops testing the UI (and may skip event handlers).

## Gotchas
- `execute_script` without `return` yields `None` (ran: `document.title` gave `None`, `return document.title` gave the title).
- `execute_async_script` that never calls its callback raises `TimeoutException: script timeout` after `set_script_timeout` seconds (ran with 1 s).
- Cookie expiry is seconds since epoch (`expiry` key).
- HttpOnly cookies are visible to WebDriver but not to `document.cookie` (ran: `get_cookie('hto')` returned it, `document.cookie` was empty).

## Verify
Cookie-based login tests land on the authenticated page; grep for `.click()` in JS strings and justify each.
