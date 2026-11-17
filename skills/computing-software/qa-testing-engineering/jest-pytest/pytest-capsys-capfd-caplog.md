---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-capsys-capfd-caplog
name: pytest-capsys-capfd-caplog
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest, capsys, capfd, caplog, pytest-plugins, logging-assertions, output-capture, python]
level: practitioner
status: verified
description: "Assert on printed output and log records in pytest with capsys, capfd and caplog: reading captured text, log levels, logger names and disabling capture."
sources:
  - https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html
  - https://docs.pytest.org/en/stable/how-to/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest capsys, capfd and caplog

**Goal:** test what code prints and logs without patching `print` or loggers.

## stdout/stderr
```python
def test_cli_prints_summary(capsys):
    main(["report", "--dry-run"])
    out, err = capsys.readouterr()          # resets the buffer
    assert "3 orders" in out
    assert err == ""
```
- `capsys`: Python-level `sys.stdout/stderr`. `capfd`: file descriptors 1/2, catches output from C extensions and subprocesses inheriting FDs. `capsysbinary`/`capfdbinary` for bytes.
- `with capsys.disabled(): print("visible in terminal")` for debugging.
- CLI: `-s` (`--capture=no`) disables capture globally.

## Logging
```python
import logging
def test_warns_on_retry(caplog):
    caplog.set_level(logging.WARNING, logger="shop.payments")
    pay(order, attempts=2)
    assert any(r.levelname == "WARNING" and "retrying" in r.getMessage() for r in caplog.records)
    assert caplog.record_tuples[-1] == ("shop.payments", logging.WARNING, "retrying payment 2/3")
```
- `caplog.text` (formatted), `caplog.records` (LogRecord objects), `caplog.messages`, `caplog.clear()`.
- `caplog.get_records("setup")` for logs during fixture setup.
- Config: `log_level = INFO` in pytest.ini; `log_cli = true` streams logs live.

## Gotchas
- Loggers with `propagate = False` (some frameworks configure that) never reach caplog's root handler; set the level on the specific logger or re-enable propagation in tests.
- Asserting the exact full message couples tests to wording; assert key parts.
- `capsys` and `capfd` cannot be used in the same test (setup error: "cannot use capfd and capsys at the same time").

## Verify
Remove the log call in the code: the caplog assertion fails.
