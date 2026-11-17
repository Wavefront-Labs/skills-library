---
id: computing-software.systems-network-administration.paperless-ngx.upgrade-docker
name: upgrade-docker
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, upgrade, docker-compose-pull, backup, migrations, v3]
level: practitioner
status: docs-checked
description: "Upgrade a Docker Paperless-ngx install safely: back up, stop, pull, start, and handle the v3 prerequisite and database upgrades."
sources:
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading a Docker install

1. Make sure no active processes (like consumption) are running, then make a backup (see "Making backups" in the administration docs).
2. Ensure Paperless is stopped:
```bash
cd /path/to/paperless
docker compose down
```
3. If you pull the image, run (in the foreground):
```bash
docker compose pull
docker compose up
```
The Docker Compose files refer to `latest`, which is always the latest stable release. If you built the image yourself, run `git pull`, `docker compose build`, `docker compose up`.

Running `docker compose up` also applies any new database migrations. When everything looks healthy, press Ctrl+C once to stop gracefully, then start with `-d` to run in the background.

## Moving to v3
- v3 can only be upgraded to from version 2.20.15; upgrade older installs to 2.20.15 first.
- Read the migration guide before upgrading: `PAPERLESS_SECRET_KEY` and `PAPERLESS_DBENGINE` are now required settings, OCR settings were redesigned, and pre/post-consume scripts lose positional arguments.
- Existing task history is dropped during the upgrade; no user action is required.
- Decrypt any encrypted documents with `decrypt_documents` first; encryption support is gone.

## Database server upgrades
Paperless-ngx is compatible with Django-supported versions of PostgreSQL and MariaDB, and it is generally safe to update them. Always take a backup and follow your database's own instructions for major version upgrades. As of Paperless-ngx v2.18 the minimum supported PostgreSQL version is 14. Alternatively use the exporter and importer with `--data-only`, after creating a new database on the updated version. Do not change any settings, especially paths, while doing this, or there is a risk of data loss.

## Bare metal
After unpacking the new release: update system dependencies, run `pip install -r requirements.txt`, then in `src` run `python3 manage.py migrate`, `python3 manage.py document_index reindex --if-needed` and `python3 manage.py document_llmindex migrate`. Unpacking an archive over an existing install does not remove deleted files, which can cause errors such as `NodeNotFoundError` during `migrate`; remove the previous source tree first (keeping `media`, `data`, `consume` and your configuration).

## Checked
Date: 2026-11-07
Pages read in full: administration (docs/administration.md), migration-v3 (docs/migration-v3.md).
Corrections: "exporter or volume copy" was not on the page and was replaced with a pointer to the backups section; the bare-metal line was rewritten to the documented steps and the leftover-files warning; the v3 list was aligned to the migration page wording.
Method: documentation only; no commands were run.
