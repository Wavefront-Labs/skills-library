---
id: computing-software.web-development.ghost.ghost-cli-doctor-ls-and-logs
name: ghost-cli-doctor-ls-and-logs
category: computing-software
field: web-development
product: ghost
tags: [ghost, ghost-cli, ghost-doctor, ghost-ls, logs, troubleshooting]
level: practitioner
status: docs-checked
description: "Diagnose a Ghost install with ghost doctor, find instances with ghost ls and read access and error logs with ghost log."
sources:
  - https://github.com/TryGhost/docs/blob/main/ghost-cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find out what is wrong with a self-hosted Ghost site.

`ghost doctor` checks the system for problems when installing or updating. The CLI runs it automatically on install, update, start and setup, and you can run it manually. Subchecks: `ghost doctor startup` (config file exists and validates) and `ghost doctor setup` (setup process succeeded). `--no-check-mem` disables the memory availability checks.

`ghost ls` lists every Ghost site and its status from the `~/.ghost/config` file, useful when you forget where an instance lives or run several.

`ghost log` shows the site's access and error logs (not the CLI's). By default it prints the last 20 lines of the access log for the site in the current folder. Logs are written to `content/logs` as an access log and an error log (`.error.log`), named after the site descriptor pattern `[proto]__[url]__[env]` (for example `https__mysite_com__production`); they rotate so numbered files appear. Options: `-n` or `--number` lines, `-e` or `--error`, `-f` or `--follow`.

`ghost uninstall` completely removes an install, including its content folder and data, and must run in the install directory; back up first.

Some output never reaches the log files, so `ghost run` (runs Ghost directly, output in the terminal) is the debugging fallback; `ghost log` needs file logging enabled.

Verify: `ghost ls` reports the site as running after a fix.

## Checked

2026-11-04. Confirmed: doctor behaviour, startup and setup subchecks, --no-check-mem, ls source and purpose, log defaults, log file layout and options, uninstall effects, ghost run (Ghost CLI page). Removed: the "better than deleting the folder" and "setup restarts after interruption" claims and the invented troubleshooting order.

Method: documentation only; no commands were run.
