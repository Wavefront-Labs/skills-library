---
id: computing-software.data-engineering.metabase.environment-variables
name: environment-variables
category: computing-software
field: data-engineering
product: metabase
tags: [environment-variables, mb-prefix, precedence, config-key, java-d]
level: practitioner
status: docs-checked
description: "Configure Metabase with MB_ environment variables: naming, types and defaults, precedence over admin settings, how to set them per launch style, and selected gotchas."
sources:
  - https://www.metabase.com/docs/latest/configuring-metabase/environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Naming: all variables use the `MB_` prefix in uppercase, such as `MB_SITE_NAME`. Each entry lists a type (string, integer, boolean, json, keyword, csv and others) and a default; a default of `null` means unset. Many entries also list a config-file key in kebab case, such as `admin-email`. Entries marked "Environment variable only" cannot be set in Admin settings or a config file.

Precedence: environment variables take precedence over Admin settings, and they are not written to the application database.

Setting them: `export`, `set` or `$env:` for the JAR; `java -D` flags; `docker run -e` for containers.

Gotchas:
- Many variables need a Pro or Enterprise plan.
- Some are deprecated, such as `MB_ENABLE_EMBEDDING`.
- `MB_DB_QUERY_TIMEOUT_MINUTES` does not apply to transforms, which use `MB_TRANSFORM_TIMEOUT`.
- `MB_AUDIT_MAX_RETENTION_DAYS` has a 30-day minimum, and `0` keeps data indefinitely.
- `MB_AGGREGATED_QUERY_ROW_LIMIT` must be less than 1048575.
- `MB_LLM_PROVIDERS` is read-only in the UI when set through the environment.
- On Metabase Cloud you must contact support to change environment variables.

## Checked
2026-11-03. Confirmed against the Metabase docs page Configuring Metabase, Environment variables: MB_ prefix, type and default listing, environment-only entries, precedence and not stored in the application database, ways to set them (export, set, $env:, java -D, docker -e), MB_ENABLE_EMBEDDING deprecation, MB_DB_QUERY_TIMEOUT_MINUTES versus MB_TRANSFORM_TIMEOUT, MB_AUDIT_MAX_RETENTION_DAYS minimum 30, MB_AGGREGATED_QUERY_ROW_LIMIT bound, MB_LLM_PROVIDERS read-only, Cloud support contact. Removed the claim that application database variables are not listed (MB_DB_* entries are on the page).
Method: documentation only; no commands were run.
