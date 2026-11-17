---
id: computing-software.systems-network-administration.paperless-ngx.v3-migration-checklist
name: v3-migration-checklist
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, v3-migration, upgrade-checklist, breaking-changes, encryption, whoosh]
level: advanced
status: docs-checked
description: "A checklist of v3 breaking changes: required settings, removed variables, search and OIDC changes, and encryption removal."
sources:
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paperless-ngx v3 migration checklist

Upgrade to v3 only from version 2.20.15; upgrade older installs to 2.20.15 first.

## Required before starting
- Set `PAPERLESS_SECRET_KEY` explicitly; it is now required. Reusing the previous built-in default key preserves existing sessions and tokens, while a new random value invalidates them.
- Set `PAPERLESS_DBENGINE` to `postgresql` or `mariadb` if you use either; SQLite users need no change.
- Decrypt documents with `decrypt_documents` before upgrading; document and thumbnail encryption is no longer supported.

## Removed or renamed
- OCR: `PAPERLESS_OCR_MODE=skip` and `skip_noarchive`, and `PAPERLESS_OCR_SKIP_ARCHIVE_FILE`, are removed. Use `PAPERLESS_OCR_MODE` (`auto`, `force`, `redo`, `off`) plus `PAPERLESS_ARCHIVE_FILE_GENERATION` (`auto`, `always`, `never`).
- Database: `PAPERLESS_DBSSLMODE`, `DBSSLROOTCERT`, `DBSSLCERT`, `DBSSLKEY`, `DB_POOLSIZE` and `DB_TIMEOUT` are replaced by `PAPERLESS_DB_OPTIONS`. The deprecated variables still work for now and log a warning at startup.
- Consumer: `CONSUMER_POLLING` is now `CONSUMER_POLLING_INTERVAL`, and `CONSUMER_INOTIFY_DELAY` is now `CONSUMER_STABILITY_DELAY`. `CONSUMER_POLLING_DELAY` and `CONSUMER_POLLING_RETRY_COUNT` are removed. `CONSUMER_IGNORE_PATTERNS` is now regex, not fnmatch, and your entries are added to the defaults.
- `CONSUMER_BARCODE_SCANNER` is removed; zxing-cpp is the only backend, and the `libzbar0` / `libzbar-dev` packages are no longer needed.
- Pre- and post-consume scripts no longer receive positional arguments; use the environment variables such as `DOCUMENT_SOURCE_PATH`.

## Behaviour changes
- Duplicates are no longer rejected unless `PAPERLESS_CONSUMER_DELETE_DUPLICATES=true`.
- The search index moves from Whoosh to Tantivy and is rebuilt from scratch on first start. Use `notes.note:` and `custom_fields.value:`. Saved views with explicit `note:` or `custom_field:` prefixes are migrated, but unqualified terms in saved views stop matching note and custom field content.
- If OIDC login fails at the callback with `invalid_client`, add `token_auth_method` (for example `client_secret_basic`) to the provider `settings`.
- Behind a reverse proxy, you may need `PAPERLESS_TRUSTED_PROXIES`, `PAPERLESS_ALLAUTH_TRUSTED_PROXY_COUNT` or `PAPERLESS_ALLAUTH_TRUSTED_CLIENT_IP_HEADER` to avoid `403 Forbidden` on login.
- Existing task history is dropped during the upgrade.
- On CPUs without SSE4.2, the classifier crashes with `SIGILL`; set `PAPERLESS_TRAIN_TASK_CRON=disable`.
- `MailRule.maximum_age` values above 32767 are clamped to 32767 during migration.

Removed OCR variables still present in the environment log a startup warning.

## Checked
Date: 2026-11-07
Pages read in full: migration-v3 (source docs/migration-v3.md from the paperless-ngx repository).
Removed as unconfirmed on that page: "back up first", the administration source, "no default" for the secret key, and a blanket claim that startup logs warn about all removed variables (the page states this for removed OCR variables and for deprecated DB variables).
Method: documentation only; no commands were run.
