---
id: computing-software.devops-ci-cd.gitea.cli-admin-user
name: cli-admin-user
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-admin-user-create, gitea, admin-user-list, generate-access-token, must-change-password, random-password, change-password]
level: practitioner
status: docs-checked
description: "Manage Gitea users from the CLI: admin user create with random password and access token, change-password, must-change-password, delete, list, generate-access-token."
sources: ["https://docs.gitea.com/administration/command-line/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# `gitea admin user` commands

Global options on any command: `--config/-c`, `--work-path/-w` (default binary path or `$GITEA_WORK_DIR`), `--custom-path/-C` (default `WorkPath/custom` or `$GITEA_CUSTOM`). The config default is `CustomPath/conf/app.ini`.

- `gitea admin user list [--admin]`: list users, optionally only admins.
- `gitea admin user create --username NAME --password PW --email ADDR [--admin] [--access-token] [--must-change-password=false] [--random-password] [--random-password-length N]`
  - `--name` is the old spelling; use `--username` (since 1.9.0).
  - `--must-change-password` defaults to true, so a created user must set a new password at first login; disable with `=false`.
  - `--random-password` discards `--password` and generates one (default length 12).
  - `--access-token` also creates a token for the user (default false).
- `gitea admin user change-password -u NAME -p NEWPW [--must-change-password=false]` (default forces a change at next login).
- `gitea admin user must-change-password [username...] [--all/-A] [--exclude/-e user] [--unset]` forces (or with `--unset` revokes) a forced change.
- `gitea admin user delete` needs one of `--id`, `--username`, `--email`; if several are given all must match.
- `gitea admin user generate-access-token -u NAME -t TOKENNAME [--scopes ...]`. Scopes are comma separated `[read|write]:<block>` or `all`, where `<block>` is a group on the API swagger page (for example `repo`).

Example: `gitea admin user create --username myname --password asecurepassword --email me@example.com`.

## Related maintenance
`gitea admin regenerate hooks` rewrites git hooks in every repository; `gitea admin regenerate keys` rewrites `authorized_keys`. Both are what you run after moving or renaming the binary (see `gitea-from-binary`).
`gitea actions generate-runner-token [-s owner[/repo]]` prints a registration token for `act_runner`; no scope makes a global runner (see `gitea-act-runner`).

## Checked

2026-11-03: read https://docs.gitea.com/administration/command-line/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
