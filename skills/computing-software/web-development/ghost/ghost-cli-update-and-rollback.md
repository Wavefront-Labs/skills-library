---
id: computing-software.web-development.ghost.ghost-cli-update-and-rollback
name: ghost-cli-update-and-rollback
category: computing-software
field: web-development
product: ghost
tags: [ghost, ghost-cli, update, rollback, ghost-update, upgrade]
level: practitioner
status: docs-checked
description: "Update a Ghost-CLI site with ghost update, pin versions, roll back a failed upgrade and know when major updates need extra steps."
sources:
  - https://github.com/TryGhost/docs/blob/main/ghost-cli.mdx
  - https://github.com/TryGhost/docs/blob/main/update.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upgrade Ghost safely.

Releases ship weekly according to the update page; check with `ghost check-update`. If you are on the latest major (6.x), run `ghost update`. For safety run `ghost backup` first.

Variants:
- `ghost update` for the latest version.
- `ghost update 2.15.0` for a specific version (1.0.0 or higher).
- `ghost update --rollback` if an upgrade goes wrong.
- `ghost update --force` to re-download the latest version, `ghost update <version> --force` for a specific one.
- `--no-restart` to skip the restart, `--no-auto-rollback` to disable automatic rollback on failure, `--zip path/to/file.zip` to update from a zip, `--no-check-mem` to skip memory checks in doctor.

Major updates (every 12-18 months, per the CLI page) break backwards compatibility and need a more involved upgrade, including backups and theme compatibility; follow the update documentation. If `ghost update` errors, use `ghost run` to debug.

Update guidance: 5.x with MySQL and 3.x or 4.x with MySQL use the update path; 3.x or 4.x with SQLite, SQLite in production on any version, and anything older than 3.0 are recommended for a reinstall instead.

Verify: `ghost ls` shows the new version running.

## Checked

2026-11-04. Confirmed: weekly releases, ghost check-update, 6.x latest major, every ghost update variant and flag, ghost run for debugging, the update-path table (Ghost CLI and update pages). Removed: "update to the latest minor first" and the Node and CLI minimum-version advice, which neither page states.

Method: documentation only; no commands were run.
