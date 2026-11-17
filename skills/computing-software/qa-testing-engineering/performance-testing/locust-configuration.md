---
id: computing-software.qa-testing-engineering.performance-testing.locust-configuration
name: locust-configuration
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [locust-conf, locust-configuration, locust-cli, locust-env-vars]
level: practitioner
status: verified
description: "Configure Locust runs via locust.conf, pyproject, LOCUST_* env vars and CLI flags in the documented precedence, including host, users, spawn rate, run time and custom arguments."
sources:
  - https://docs.locust.io/en/stable/configuration.html
  - https://docs.locust.io/en/stable/extending-locust.html#custom-arguments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration (locust.conf, env vars, CLI)

## Precedence (lowest to highest)
`~/.locust.conf` -> `./locust.conf` -> `pyproject.toml [tool.locust]` -> file given by `--config` -> environment variables (`LOCUST_*`) -> command-line arguments. Later wins.
The docs page states a different order (pyproject first, then locust.conf), but Locust 2.47.0 source (`DEFAULT_CONFIG_FILES`) and a run with conflicting `users` values in all three files agree with the order above: `pyproject.toml` beat `./locust.conf`, which beat `~/.locust.conf`. Do not define the same key in both `locust.conf` and `pyproject.toml`.

## locust.conf
```ini
locustfile = locustfiles/checkout.py
host = https://staging.example.com
users = 500
spawn-rate = 20
run-time = 30m
headless = true
csv = results/checkout
html = results/checkout.html
loglevel = INFO
```
pyproject:
```toml
[tool.locust]
locustfile = "locustfiles/checkout.py"
users = 500
spawn-rate = 20
```

## Env vars
`LOCUST_HOST`, `LOCUST_USERS`, `LOCUST_SPAWN_RATE`, `LOCUST_RUN_TIME`, `LOCUST_HEADLESS=true`, `LOCUST_LOCUSTFILE`, `LOCUST_TAGS`, `LOCUST_CSV`, `LOCUST_EXIT_CODE_ON_ERROR` (the flag name upper-cased with a `LOCUST_` prefix). Handy in containers and CI matrices. On Windows set them with `set NAME=value` (cmd) or `$env:NAME` (PowerShell).

## Custom arguments
```python
from locust import HttpUser, events, task

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--tenant", type=str, env_var="LOCUST_TENANT", default="demo", help="Tenant id")
    parser.add_argument("--api-key", is_secret=True, default="", help="masked in web UI")

class Api(HttpUser):
    @task
    def orders(self):
        self.client.get(f"/t/{self.environment.parsed_options.tenant}/orders")
```
Custom args appear in the web UI start form (`include_in_web_ui=True` default; the page's data lists `tenant` and a secret `api_key`). Precedence applies to them too: `LOCUST_TENANT=acme` or `--tenant cli` both reached `environment.parsed_options.tenant`, CLI winning over env.

## Useful flags
`--stop-timeout 30` (`-s`, let tasks finish), `--exit-code-on-error 1` (exit code used when the run had failures; default is 1, `0` ignores them), `--reset-stats` (after ramp-up), `-T/--tags` and `-E/--exclude-tags`, `--class-picker` (choose User and Shape classes in the UI), `--processes 4` (fork workers on one machine; added in Locust 2.19, needs `fork()` so it is not available on Windows).

## Gotchas
- `-u`, `-r` and `-t` only take effect with `--headless` or `--autostart` (autostart keeps the web UI); otherwise start the run from the web UI form.
- Spawn rate too high (hundreds/s) floods the target with connection setup and the generator with greenlet churn.

## Verify
Custom args do not appear in `locust --help`; check them in the web UI start form or print `environment.parsed_options` in a `test_start` listener. The headless banner logs the run-time limit, and the final stats show the effective user count.

## Checked
Locust 2.47.0 (PyPI latest at review) in a Windows scratch venv against a local stdlib HTTP server, plus fetched docs.
- Run: conflicting `users` in `~/.locust.conf` (USERPROFILE pointed at a scratch folder), `./locust.conf` and `pyproject.toml`: precedence is home < locust.conf < pyproject < `--config` < env < CLI (pyproject won over locust.conf, contradicting the docs note); `DEFAULT_CONFIG_FILES` read from the installed source. Custom args (`--tenant`, `LOCUST_TENANT`, `--api-key`) parsed and shown in the web UI payload with `is_secret`; they are absent from `--help`. `--exit-code-on-error` flag and run exit codes (1 on failures, 0 with `--exit-code-on-error 0`). Flag existence from `locust --help`: `--stop-timeout`, `--tags`, `-E`, `--class-picker`, `--processes`, `--reset-stats`.
- Fetched: docs.locust.io configuration page (env var table, `--run-time` only with headless/autostart, `--processes` not on Windows) and the Locust changelog (`--processes` added 2.19.0, `is_secret` 2.15.0).
- `--processes` behaviour is as documented (fetched); it cannot run on Windows by design.
