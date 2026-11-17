---
id: computing-software.qa-testing-engineering.playwright.pytest-playwright-python
name: pytest-playwright-python
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [pytest-playwright, playwright-python, pytest, browser-automation, python-e2e]
level: practitioner
status: docs-checked
description: "Write Playwright tests in Python with pytest-playwright: page and context fixtures, CLI options for browsers and tracing, expect assertions, base URL and parallel runs."
sources:
  - https://playwright.dev/python/docs/test-runners
  - https://playwright.dev/python/docs/test-assertions
  - https://github.com/microsoft/playwright-pytest
  - https://playwright.dev/python/docs/browsers
  - https://playwright.dev/python/docs/trace-viewer
  - https://playwright.dev/python/docs/auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright for Python with pytest-playwright

**Goal:** Playwright's browser automation inside a pytest suite, reusing pytest fixtures and plugins.

## Install and run
```bash
pip install pytest-playwright
playwright install --with-deps chromium
pytest --browser chromium --browser firefox --headed --slowmo 200
pytest --base-url https://staging.example.test --tracing retain-on-failure --screenshot only-on-failure --video retain-on-failure
pytest --numprocesses auto        # needs pip install pytest-xdist
```
Artifacts land in `test-results/` (`--output` changes it); `--tracing`, `--video` and `--screenshot` default to off. Open traces with `playwright show-trace trace.zip`.

## Tests
```python
import re
from playwright.sync_api import Page, expect

def test_checkout_total(page: Page):
    page.goto("/shop")                      # relative to --base-url
    page.get_by_role("button", name="Add Beans").click()
    page.get_by_role("link", name="Basket").click()
    expect(page.get_by_test_id("total")).to_have_text("£12.50")
    expect(page).to_have_url(re.compile(r".*/basket"))
```
`expect` retries until timeout (default 5 s; `expect.set_options(timeout=10_000)`).

## Fixtures
- Function scope: `page`, `context`. Session scope: `browser`, `browser_type`, `playwright`.
- Override context options:
```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "en-GB", "viewport": {"width": 1280, "height": 720},
            "storage_state": "auth/member.json"}
```
- Marks: `@pytest.mark.skip_browser("webkit")`, `@pytest.mark.only_browser("chromium")`, `@pytest.mark.browser_context_args(timezone_id="Europe/Berlin")`.

## Async
Install `pytest-playwright-asyncio` for async fixtures; it needs `pytest-asyncio>=0.26.0`, `asyncio_default_test_loop_scope = session` in the pytest config, and `@pytest.mark.asyncio(loop_scope="session")` on async tests. Do not mix sync and async APIs.

## Gotchas
- CLI options apply only to the default `browser`, `context` and `page` fixtures, not to ones you create with `browser.new_context()`.
- `pytest-base-url` provides `--base-url`; set it in `pytest.ini` addopts for CI.

## Verify
Suite runs across two browsers in CI, failures attach traces, and fixtures provide auth state without UI login per test.

## Checked
2026-10-31. Confirmed on the Playwright Python pages (Pytest Plugin Reference, Assertions, Browsers, Trace Viewer, Authentication): `--browser`, `--headed`, `--slowmo`, `--tracing`, `--video`, `--screenshot` values and defaults, `--output` default `test-results`, fixture names and scopes, `skip_browser`, `only_browser` and `browser_context_args` marks, `--base-url` via pytest-base-url, `playwright install --with-deps chromium`, `playwright show-trace trace.zip`, `storage_state`, 5 s default assertion timeout and `expect.set_options(timeout=...)`, and the async fixture requirements. Changed `-n auto` to the documented `--numprocesses auto`. Removed the unconfirmed sync-in-event-loop gotcha and the `pytest-asyncio` with `async_playwright` route.
Method: documentation only; no commands were run.
