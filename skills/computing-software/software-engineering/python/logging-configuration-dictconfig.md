---
id: computing-software.software-engineering.python.logging-configuration-dictconfig
name: logging-configuration-dictconfig
category: computing-software
field: software-engineering
product: python
tags: [python, python-stdlib, python-logging, dictconfig, logging-handlers, structured-logging, library-logging, py-logging]
level: practitioner
status: verified
description: "Configure Python logging properly: logger hierarchy, dictConfig, handlers and formatters, JSON output, library NullHandler etiquette and non-blocking queue handlers."
sources:
  - https://docs.python.org/3/howto/logging.html
  - https://docs.python.org/3/library/logging.config.html
  - https://docs.python.org/3/howto/logging-cookbook.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Logging configuration with dictConfig

**Goal:** one place configures logging for the application; libraries only emit; output is parseable in production.

## 1. Rules
- Libraries: `log = logging.getLogger(__name__)` and never configure handlers or levels. Optionally `logging.getLogger("mylib").addHandler(logging.NullHandler())`.
- Applications: configure once at startup (`main()`), not at import time.
- Use lazy formatting: `log.info("user %s logged in", uid)`, not f-strings (formatting skipped when the level is disabled, and aggregators can group by template).
- `log.exception("...")` inside `except` adds the traceback.

## 2. dictConfig
```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,          # True silently mutes loggers created before config
    "formatters": {
        "plain": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"},
        "json": {"()": "pythonjsonlogger.json.JsonFormatter",
                 "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json", "stream": "ext://sys.stdout"},
    },
    "loggers": {
        "urllib3": {"level": "WARNING"},
        "myapp": {"level": "DEBUG"},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
logging.config.dictConfig(LOGGING)
```
Handlers only on root; child loggers propagate up. Adding handlers to children too duplicates lines.

## 3. Levels and filtering
A record must pass the logger's effective level and then each handler's level. Set noisy third-party loggers to WARNING by name. Env-driven level: `"level": os.getenv("LOG_LEVEL", "INFO")`.

## 4. Context
```python
log = logging.LoggerAdapter(logging.getLogger(__name__), {"request_id": rid}, merge_extra=True)   # merge_extra: 3.13+
log.info("charged", extra={"amount": 42})     # extra keys become record attributes (JSON fields)
# without merge_extra=True the adapter's dict replaces the call-site extra and "amount" is silently dropped
```
For request-scoped context across calls, a `logging.Filter` reading a `contextvars.ContextVar` adds fields to every record.

## 5. Non-blocking handlers
Slow handlers (network, file on NFS) block the caller. Use `QueueHandler` + `QueueListener` (3.12+: `"class": "logging.handlers.QueueHandler", "handlers": [...]` in dictConfig).

## Gotchas
- `logging.basicConfig()` does nothing if root already has handlers (e.g. a library or framework configured it); `force=True` replaces them.
- `extra` keys that clash with LogRecord attributes (`message`, `args`, `name`) raise `KeyError`.
- `print()` in services bypasses levels and structure; replace it.
- Containers: log to stdout, let the platform collect; avoid `RotatingFileHandler` inside containers.
- uvicorn/gunicorn/Django install their own config; integrate via their `log_config`/`LOGGING` settings rather than fighting them.

## Verify
- Start the app with `LOG_LEVEL=DEBUG` and check each line is valid JSON (`| jq .`), no duplicates, and third-party noise suppressed.
## Checked
- Python 3.14.0 on Windows: `dictConfig` with `disable_existing_loggers: False` keeps earlier loggers working while `True` sets `disabled` on them; per-logger levels (`urllib3` WARNING hides INFO, `myapp` DEBUG shows debug) and root INFO hiding other debug; a child logger with its own handler printed each line twice; `log.exception` adds the traceback; `%s` arguments are not formatted when the level is disabled; `basicConfig()` does nothing when root has handlers and `force=True` replaces them; `extra` keys `message`, `name`, `args` raise `KeyError: Attempt to overwrite`; a `LoggerAdapter` replaces the call-site `extra` (the `amount` field vanished) unless `merge_extra=True` (3.13+); a `ContextVar` filter adds `request_id`; the `QueueHandler` `dictConfig` form works; `python-json-logger` 4.2.0 provides `pythonjsonlogger.json.JsonFormatter` and emits `extra` fields. uvicorn/gunicorn/Django integration and the `jq` pipe were not run.
Linux pass (Python 3.14.8 standalone musl build in a WSL2 busybox distro): every check above gave the same result as on Windows.
