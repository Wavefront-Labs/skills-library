---
id: computing-software.qa-testing-engineering.selenium.pytest-webdriver-fixtures
name: pytest-webdriver-fixtures
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [selenium, pytest-selenium, selenium-framework, pytest-fixtures, python, conftest, screenshot-on-failure]
level: practitioner
status: verified
description: "Run Selenium with pytest: a driver fixture with browser options from CLI flags, screenshot on failure via a hook, parallel runs with xdist and base URL config."
sources:
  - https://www.selenium.dev/documentation/webdriver/getting_started/
  - https://docs.pytest.org/en/stable/how-to/fixtures.html
  - https://docs.pytest.org/en/stable/reference/reference.html#pytest.hookspec.pytest_runtest_makereport
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest fixtures for WebDriver

**Goal:** clean Python Selenium tests with setup, teardown and failure evidence handled by pytest.

## conftest.py
```python
import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--base-url", default="http://localhost:3000")

@pytest.fixture
def base_url(request): return request.config.getoption("--base-url")

@pytest.fixture
def driver(request):
    name = request.config.getoption("--browser")
    if name == "firefox":
        opts = webdriver.FirefoxOptions()
        if request.config.getoption("--headless"): opts.add_argument("-headless")
        drv = webdriver.Firefox(options=opts)
    else:
        opts = webdriver.ChromeOptions()
        if request.config.getoption("--headless"): opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1366,900")
        drv = webdriver.Chrome(options=opts)     # Selenium Manager fetches the driver
    yield drv
    drv.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed and "driver" in item.funcargs:
        item.funcargs["driver"].save_screenshot(f"artifacts/{item.name}.png")
```

## Running
```bash
pytest --browser=firefox --headless -n 4 --junitxml=results.xml   # -n needs pytest-xdist
```

## Notes
- The `pytest-selenium` plugin (4.1.0) offers a ready-made `selenium` fixture and a `--driver` option; the hand-rolled fixture above avoids plugin coupling.
- Ran this `conftest.py` unchanged on pytest 9.1 and Selenium 4.51: `--headless` on Chrome, `--browser=firefox --headless` on Firefox, `-n 4` with pytest-xdist, and `--junitxml`.

## Gotchas
- Module/session-scoped driver fixtures speed up runs but leak state (cookies, open dialogs) between tests; clear cookies or use function scope.
- `os.makedirs("artifacts", exist_ok=True)` before saving screenshots: with no `artifacts/` folder the hook saved nothing and raised no error (ran); with the folder, `-n 4` wrote `artifacts/test_fail.png`.

## Verify
A deliberately failing test produces a screenshot named after the test, and `-n 4` runs without shared-driver errors.
