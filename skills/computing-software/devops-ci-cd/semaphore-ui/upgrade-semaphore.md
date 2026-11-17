---
id: computing-software.devops-ci-cd.semaphore-ui.upgrade-semaphore
name: upgrade-semaphore
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [upgrade, migrate, database-migration, rollback, release, semaphore-ui]
level: practitioner
status: docs-checked
description: "Upgrade Semaphore by installing the new package or binary, and apply or roll back schema migrations."
sources:
  - https://semaphoreui.com/docs/admin-guide/upgrading
  - https://semaphoreui.com/docs/reference/cli/migrations
  - https://semaphoreui.com/docs/admin-guide/authentication/local
  - https://semaphoreui.com/docs/admin-guide/audit-log
  - https://semaphoreui.com/docs/admin-guide/metrics
  - https://semaphoreui.com/docs/introduction/security-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrade Semaphore

Goal: move to a newer release safely.

1. Back up the database (the migrations page says to do this before applying or rolling back migrations) and `access_key_encryption` (the security model page lists both as backups to keep).
2. Install the new version the same way you installed the old:
   - Package: download the newer `.deb`/`.rpm` from the Releases page and run `dpkg -i` or `yum install` on it.
   - Binary: download the new archive from the Releases page and unpack it (`tar xf` on Linux, `Expand-Archive` on Windows).

Migrations: `semaphore server`, `semaphore setup` and every command that touches the database apply pending migrations automatically. To run them without starting the server, or to roll back, use `semaphore migrate` (`--apply-to <version>` or `--undo-to <version>`, mutually exclusive). To undo migrations, run it with the newer binary before installing the older one. If a migration fails, make sure the CLI binary is the same version as the server and uses the same configuration file.

Version notes from the docs:
- 2.20 adds Argon2id password hashing (old bcrypt hashes are upgraded on next sign-in) and the metrics endpoint.
- During a rolling upgrade of an HA cluster, a task started on an upgraded node and finished on a not-yet-upgraded node has no completion audit event.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): admin-guide/upgrading.md, reference/cli/migrations.md, admin-guide/authentication/local.md and admin-guide/metrics.md. Also read admin-guide/audit-log/README.md only from line 38 to 52 (the rolling upgrade sentence) and introduction/security-model.md only around the backup bullet, not whole. Confirmed: the deb and rpm install commands, the binary archive unpack, automatic migrations, migrate flags and rollback ordering, Argon2id from 2.20 with bcrypt hashes replaced on next sign-in, the metrics endpoint since 2.20, and the HA rolling upgrade audit gap. Removed: the Docker pull step and its description mention (the upgrading page covers only packages and binaries), the restart step, the runner-API-sync advice, and the Verify step.
Method: documentation only; no commands were run.
