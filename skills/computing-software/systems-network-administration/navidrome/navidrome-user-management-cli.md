---
id: computing-software.systems-network-administration.navidrome.navidrome-user-management-cli
name: navidrome-user-management-cli
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, user-create, user-edit, user-delete, admin, library-ids, password-reset, user-list]
level: practitioner
status: docs-checked
description: "Manage Navidrome users from the command line: create, edit, list and delete, admin versus regular role, per-library access, password changes and the last-user guard."
sources: ["https://www.navidrome.org/docs/usage/admin/cli/user/", "https://www.navidrome.org/docs/usage/admin/cli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome users from the CLI

These commands need at least one admin already in the database; on a new install create the first admin in the web UI.

- `navidrome user create --username alice --email alice@example.com --admin`. It prompts twice for the password (no password flag, so a terminal or `docker run -it` is required; empty Enter cancels). Without `--library-ids` the user gets all libraries; with `--admin` the flag is ignored because admins always see all libraries. A nonexistent library ID aborts creation.
- `navidrome user create --username bob --name "Bob Smith" --library-ids 1,3`.
- `navidrome user edit --user <username-or-id>` with: `--set-admin`, `--set-regular`, `--set-password` (prompts), `--email` or `--remove-email`, `--name` or `--remove-name`, `--library-ids 1,2`. Flag pairs are mutually exclusive. `--set-admin` grants every library; `--set-regular` keeps the current libraries until you pass `--library-ids`, which replaces the list. This is the way to reset a forgotten password: `navidrome user edit --user alice --set-password`.
- `navidrome user list [-f csv|json]`: columns are id, username, name, email, admin, created, updated, last access, last login, libraries as `id:path` separated by `|`. Use it to find library IDs.
- `navidrome user delete --user alice`: no confirmation; refuses to delete the last user. Aliases: `c`, `e`, `d`.

With the Docker image, prefix with `docker compose run --rm navidrome`.

Verify: `navidrome user list --format json` shows the changed role or libraries.

## Checked

2026-11-04. Confirmed against the Navidrome `user` CLI page (flags, aliases, password prompt, library rules, list columns, last-user guard) and the CLI overview page (Docker Compose `run --rm` form). Nothing removed.

Method: documentation only; no commands were run.
