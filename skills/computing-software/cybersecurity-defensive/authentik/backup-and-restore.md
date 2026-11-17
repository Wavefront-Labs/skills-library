---
id: computing-software.cybersecurity-defensive.authentik.backup-and-restore
name: backup-and-restore
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, backup, restore, postgresql, pg-dump, static-directories]
level: practitioner
status: docs-checked
description: "What to back up for authentik: the PostgreSQL database first, then /data, /certs, /custom-templates and /blueprints, and how to restore."
sources:
  - https://docs.goauthentik.io/sys-mgmt/ops/backup-restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: be able to rebuild an authentik instance. The PostgreSQL database holds users, policies, flows and configuration; without it authentik cannot be restored.

## Database
- Back up with native tooling: `pg_dump`, `pg_dumpall` or continuous archiving. Exclude the system databases `template0` and `template1`.
- Store backups off the database host.
- Restore the database before bringing authentik back, with `pg_restore` or `psql` depending on how the dump was made, and verify it is complete before reconnecting authentik.

## Static directories (volumes)
| Directory | Holds | Notes |
| --- | --- | --- |
| `/data` | icons, flow backgrounds, uploads, CSV reports | only if not using S3; back S3 up with `aws s3 sync` |
| `/certs` | TLS certificates on the filesystem | needed only if you rely on files; certificates already imported live in the database |
| `/custom-templates` | custom UI changes | required if you changed the appearance |
| `/blueprints` | blueprints | recommended if you use custom blueprints |

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/sys-mgmt/ops/backup-restore/ (read in full); dropped the claim that downgrades are unsupported, which the page does not state.
