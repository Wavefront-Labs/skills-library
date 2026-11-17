---
id: computing-software.data-engineering.prefect.settings-and-profiles
name: settings-and-profiles
category: computing-software
field: data-engineering
product: prefect
tags: [settings, profiles, precedence, prefect-toml, config]
level: practitioner
status: docs-checked
description: "Prefect settings sources and precedence, prefect.toml and pyproject.toml layout, profiles commands and the common API settings."
sources:
  - https://docs.prefect.io/v3/concepts/settings-and-profiles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set Prefect configuration predictably.

Precedence, highest first: environment variables, `.env` in the working directory, `prefect.toml`, `pyproject.toml`, active profile, defaults.

Sources:
- env vars: any setting prefixed `PREFECT_`, for example `PREFECT_LOGGING_LEVEL="DEBUG"`
- `.env`: lines like the above (prefect>=3.0.5)
- `prefect.toml`: settings at root, `[logging]` then `level = "DEBUG"` (prefect>=3.1)
- `pyproject.toml`: under `[tool.prefect]`, `logging.level = "DEBUG"` (prefect>=3.1)

Profiles live in `~/.prefect/profiles.toml` (override with `PREFECT_PROFILES_PATH`); exactly one is active. After install the `ephemeral` profile is active.

Commands:
- `prefect profile create (--from) | delete | inspect | ls | rename | use | populate-defaults`
- `prefect config set | unset | view` (active profile)

```bash
prefect profile create new-profile --from ephemeral
prefect profile use new-profile
prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true PREFECT_LOGGING_LEVEL="ERROR"
prefect config unset PREFECT_LOGGING_LEVEL -y
```

Common settings: `api.url` (`PREFECT_API_URL`), `api.key` (`PREFECT_API_KEY`), `home`, `server.database.connection_url` (SQLAlchemy URL; SQLite and Postgres). `prefect cloud login` sets URL and key for the active profile.

## Checked

2026-11-08. Source precedence, version gates, prefect.toml and pyproject.toml layout, profile and config commands, profiles.toml location, ephemeral profile and common settings confirmed against the settings and profiles page.

Method: documentation only; no commands were run.
