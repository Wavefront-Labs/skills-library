---
id: computing-software.collaboration-platform-administration.vikunja.cli-user-management
name: cli-user-management
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, user-create-cli, user-reset-password, user-delete-now, set-admin-pro]
level: practitioner
status: docs-checked
description: "Manage Vikunja users from the CLI: create, list, update, disable, reset passwords, delete, and promote admins, with the flags and cautions for each."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All commands are `vikunja user <sub>`; in Docker prefix with `docker exec -it`.

- `list`: show all users.
- `create -u NAME -e EMAIL [-p PASS] [-a AVATAR]`: password is prompted if omitted.
- `update ID [-u] [-e] [-a]`: change username, email or avatar provider.
- `change-status ID [-d|-e]`: disable or enable; toggles when no flag is given.
- `reset-password ID`: sends a reset mail. With `-d` it sets the password directly (`-p`, else prompted; `-p` is only used with `--direct`).
- `delete ID`: only emails the user a confirmation, as the web UI does. `--now` (`-n`) deletes immediately. The page says to use with caution.
- `set-admin USER --admin|--no-admin`: requires an active Vikunja Pro licence with the admin panel feature. The last admin cannot be demoted.

## Checked

2026-11-04: all subcommands and flags checked against the CLI page (user section). Removed the "typical rescue" recipe, the "registration disabled" and "mail not configured" remarks and the "back up first" advice, none of which the page states.

Method: documentation only; no commands were run.
