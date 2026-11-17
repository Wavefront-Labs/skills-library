---
id: computing-software.qa-testing-engineering.selenium.page-load-strategy-and-timeouts
name: page-load-strategy-and-timeouts
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [page-load-strategy, selenium-timeouts, implicit-wait, script-timeout, page-load-timeout]
level: practitioner
status: verified
description: "Set Selenium page load strategy (normal, eager, none) and session timeouts (implicit, pageLoad, script), and why implicit and explicit waits must not be mixed."
sources:
  - https://www.selenium.dev/documentation/webdriver/drivers/options/#pageloadstrategy
  - https://www.selenium.dev/documentation/webdriver/drivers/options/#timeouts
  - https://www.selenium.dev/documentation/webdriver/waits/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page load strategy and timeouts

## Strategies
| Strategy | `get()` returns when | Use |
|---|---|---|
| `normal` (default) | `load` event (all subresources) | most apps (ran: `get` took 4.1 s while a 4 s image was pending) |
| `eager` | `DOMContentLoaded` | pages with slow ads/images; you then wait explicitly for elements (ran: 0.1 s on the same page) |
| `none` | immediately after navigation starts | rare; full manual waiting (ran: returned in under 0.1 s) |

```python
options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"
```

## Timeouts
```python
options.timeouts = {"implicit": 0, "pageLoad": 60000, "script": 30000}   # ms, as capabilities
driver.set_page_load_timeout(60)   # seconds, runtime
driver.set_script_timeout(30)
driver.implicitly_wait(0)
```
- `pageLoad` default 300s (ran: `driver.timeouts.page_load == 300.0`): lower it so hung pages fail in reasonable time (ran with 1000 ms: `TimeoutException: Timed out receiving message from renderer`).
- `script` default 30s: async scripts.
- `implicit` default 0. `options.timeouts = {...}` is reported back by `driver.timeouts` (ran).

## Implicit vs explicit
Selenium docs: "Do not mix implicit and explicit waits. Doing so can cause unpredictable wait times." (ran: a 1 s explicit wait for a missing element took 5.0 s with `implicitly_wait(5)` set, because each poll waited the implicit timeout). Pick **explicit waits** (`WebDriverWait`) and keep implicit at 0.

## Gotchas
- With `eager`, elements may exist before JS frameworks attach handlers; wait for an app-ready signal.
- SPAs: page load strategy only matters for full navigations, not client-side routing.
- A `TimeoutException` from `get()` leaves the page partially loaded; you can still interact (ran: `driver.title` still returned `parsed` afterwards; `window.stop()` via JS if needed).

## Verify
A page with a slow third-party script loads under `eager` in a fraction of the time and tests still pass.
