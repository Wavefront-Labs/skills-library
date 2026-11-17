---
id: computing-software.data-engineering.metabase.config-file
name: config-file
category: computing-software
field: data-engineering
product: metabase
tags: [config-file, config-yml, mb-config-file-path, env-interpolation, declarative-setup]
level: advanced
status: docs-checked
description: "Seed a self-hosted Metabase from config.yml: location, required version key, users, databases, api-keys, settings key naming, env interpolation and overwrite-on-restart."
sources:
  - https://www.metabase.com/docs/latest/configuring-metabase/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Availability: Pro and Enterprise, self-hosted only. New installs must set `MB_PREMIUM_EMBEDDING_TOKEN` at launch.

Location: `config.yml` or `config.yaml` in the directory holding the JAR, or any path in `MB_CONFIG_FILE_PATH`.

Structure: `version: 1` is required, then `config:` containing any of `settings`, `users`, `databases`, `api-keys`.

- users: `first_name`, `last_name`, `password`, `email`, `is_superuser`. On an already set-up instance the first listed user is a normal user unless `is_superuser: true`.
- databases: `name`, `engine`, `details`; uploads via `uploads_enabled`, `uploads_schema_name`, `uploads_table_prefix`.
- api-keys: `name`, `group` (`admin` or `all-users`), `creator` (an admin), `key`. Keys are `mb_` plus Base64, 12-254 characters; generate with `echo "mb_$(openssl rand -base64 32)"`. An existing key of the same name is kept; delete it first to replace it.
- settings: the env var name lowercased, `MB_` dropped, underscores to hyphens (`MB_EMAIL_FROM_NAME` becomes `email-from-name`). Not every env var is settable.

Interpolation: `"{{ env VAR_NAME }}"`, quoted, no recursive expansion. Literal braces use `"{{{ value }}}"`.

Gotchas:
- On every restart file values overwrite matching UI changes.
- Entries update existing objects rather than duplicating them.
- To skip initial sync, set `config-from-file-sync-databases: false` under `settings`, before `databases`. The page spells this key two ways, so check your version.
- The `api-key` setting only authenticates `/notify`; it creates no API key.

## Checked
2026-11-03. Confirmed against the Metabase docs page Configuring Metabase, Configuration file: Pro/Enterprise self-hosted availability, file location and MB_CONFIG_FILE_PATH, version key, user, database, uploads and api-keys fields, mb_ key format (12 to 254 characters), openssl example, existing-key behaviour, setting-name translation, env interpolation with quotes, triple braces, overwrite on restart, MB_PREMIUM_EMBEDDING_TOKEN. Nothing removed.
Method: documentation only; no commands were run.
