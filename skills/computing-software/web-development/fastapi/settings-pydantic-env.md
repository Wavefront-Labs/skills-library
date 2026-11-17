---
id: computing-software.web-development.fastapi.settings-pydantic-env
name: settings-pydantic-env
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, settings, environment-variables, pydantic-settings, dotenv, lru-cache, dependency-override]
level: practitioner
status: docs-checked
description: "Manage FastAPI configuration with pydantic-settings: env vars, .env files, a cached get_settings dependency with lru_cache, and overriding settings in tests."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/settings.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Settings and environment variables

## Rules
- Env vars are always text (`str`); conversion and validation are your code's job. Pydantic Settings does it.
- Install `pydantic-settings` (also included with `fastapi[all]`).
- Subclass `BaseSettings` with typed attributes and defaults; `Field()` validation works. Env vars are read case-insensitively (`APP_NAME` fills `app_name`) and converted (e.g. `int`).
- Set variables per command, e.g. in Bash `ADMIN_EMAIL="..." APP_NAME="..." fastapi run main.py`, or in PowerShell with `$Env:NAME = "..."` first.
- Settings can live in their own module (e.g. `config.py`).

## Settings as a dependency
- Instead of a global `settings` object, the docs show a `get_settings()` function returning `config.Settings()` and used with `Depends`, which makes tests easy to override.
- In tests, override that dependency with a different `Settings` object.

## .env files
- Add `python-dotenv`. Declare `model_config` with `env_file` set to the file name (e.g. `.env`, lines like `APP_NAME="..."`).
- Every `Settings()` call re-reads the file, so decorate `get_settings()` with `functools.lru_cache`: it runs once and later calls return the same object. It still works as an overridable dependency.

## Verify
Run with env vars set and return the values from a path operation.

## Checked

Read the full advanced/settings.md source page. Confirmed env vars are str, pydantic-settings install and its inclusion in fastapi[all], BaseSettings case-insensitive reading, the Bash and PowerShell examples, settings in a dependency with test override, python-dotenv with model_config env_file, and lru_cache creating Settings once. Reworded the global-instance rule, which the page presents as an option for testability rather than a prohibition.

Method: docs-only read of cited pages, 2026-11-08
