---
id: computing-software.collaboration-platform-administration.vikunja.cli-dump-restore-migrate
name: cli-dump-restore-migrate
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, dump-command, restore-command, preserve-config, migrate-rollback]
level: practitioner
status: docs-checked
description: "Use the Vikunja CLI to dump an instance to a zip, restore it elsewhere with --preserve-config, and list or roll back database migrations."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vikunja dump` writes a zip containing the config, version, all files and the full database. Flags: `-p/--path` for the folder (default: configured root path or binary location), `-f/--filename` (`.zip` added if missing; default `vikunja-dump_YYYY-MM-DD_HH-II-SS.zip`).

`vikunja restore <dump.zip>` restores one. `--preserve-config` keeps the current config instead of the dumped one; use it when moving to an environment with different database settings or file paths.

Migration (schema) commands:
- `vikunja migrate`: run all pending database migrations.
- `vikunja migrate list`: list all migrations.
- `vikunja migrate rollback -n <id>`: roll back until the given migration id.

In Docker, run these in the container: `docker exec <container> /app/vikunja/vikunja dump`.

## Checked

2026-11-04: checked against the CLI page (dump, restore, migrate sections). Removed advice about secrecy of the zip, rollback needing a fresh backup and an older binary, and copying the zip out of the container; the page states none of it.

Method: documentation only; no commands were run.
