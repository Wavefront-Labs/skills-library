---
id: computing-software.web-development.ghost.ghost-cli-overview-and-commands
name: ghost-cli-overview-and-commands
category: computing-software
field: web-development
product: ghost
tags: [ghost, ghost-cli, nginx, systemd, mysql, administration]
level: practitioner
status: docs-checked
description: "Ghost-CLI overview: install with npm, global flags and the command set (install, setup, start, stop, restart, update, backup, doctor, ls, log, config)."
sources:
  - https://github.com/TryGhost/docs/blob/main/ghost-cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage a self-hosted Ghost site from the command line.

Install or update the CLI: `sudo npm install -g ghost-cli@latest` on a production server using a non-root user. Using `@latest` installs or updates with one command.

What it does: checks environment problems, creates a logical folder structure, supports production or development installs, handles upgrades and rollbacks, user management and permissions, configures Ghost, NGINX, MySQL and systemd, and gives access to log files.

Useful global flags: `--help` or `-h`, `--verbose` or `-V` (debug logging), `--version` or `-v`, `--dir path/to/directory`, `--no-prompt`, `--no-color`.

Commands documented: `ghost config` (create a config file, or get or set a key such as `ghost config url https://example.com`), `ghost install`, `ghost setup`, `ghost start`, `ghost stop`, `ghost restart`, `ghost update`, `ghost backup`, `ghost doctor`, `ghost ls`, `ghost log`, `ghost uninstall` and `ghost help`; the help output also lists `ghost run`, `ghost migrate`, `ghost buster` and `ghost version`.

Commands such as `ghost start` and `ghost restart` must run in the site's directory or be passed `--dir`.

See the other ghost-cli skills for update, backup, doctor and logs.

Verify: `ghost -v` prints the CLI and Ghost versions.

## Checked

2026-11-04. Confirmed: install and update command, feature list, global flags, config forms, the command list including the help output (Ghost CLI page). Removed: the blanket "always run from the install directory" rule, narrowed to the commands the page names.

Method: documentation only; no commands were run.
