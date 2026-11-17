---
id: computing-software.devops-ci-cd.earthly.earthly-account-org-project-commands
name: earthly-account-org-project-commands
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, account, org, project, create-token, earthly-token, invite, member]
level: practitioner
status: docs-checked
description: "Register and log in to an Earthly account, create CI tokens, and manage organizations and projects with earthly account, org and project subcommands."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# earthly account, org and project

## Account
Register in two steps: first run with only the email (a token is emailed), then repeat with the token.
```
earthly account register --email <email>
earthly account register --email <email> --token <email-verification-token> [--password <password>] [--public-key <public-key>]
```
Login variants:
```
earthly account login
earthly account login --email <email>
earthly account login --email <email> --password <password>
earthly account login --token <token>
```
With no email or token, login uses registered public keys. `account logout` removes cached login from `~/.earthly/auth.token`. Key commands: `list-keys`, `add-key [<public-key>]`, `remove-key <public-key>`. Password reset: `account reset --email <email> [--token <token>]` (first run emails a token, second run prompts for a new password).

## Tokens for CI
```
earthly account create-token [--write] [--expiry <expiry>] [--overwrite] <token-name>
```
Tokens are read-only unless `--write` is given, never expire unless `--expiry` (YYYY-MM-DD or never) is set, and an existing name is only replaced with `--overwrite`. `list-tokens` and `remove-token <token>` manage them. `export EARTHLY_TOKEN=...` forces earthly to use that token, overriding any logged-in session.

## Organizations
`org create <org-name>`, `org list` (or `ls`), `org list-permissions <org-name>`, `org invite <email>` (options `--name`, `--permission` read/write/admin, `--message`), `org revoke <org-path> <email>`, `org members (ls|update|rm)`, `org select <org-name>`, `org unselect`.

Default org precedence: `--org` argument, then `EARTHLY_ORG`, then the setting from `org select`.

## Projects
`project [--org <organization-name>] (ls|create <project-name>|rm|member)`; `rm` takes `--force`. Member commands take `--project <project-name>`: `member add` and `member update` take `<user-email> <permission>`, `member rm` takes `<user-email>`, and `member ls` takes no argument; project access levels are read, read+secrets, write and admin.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthly-command/earthly-command.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: made the project member command arguments exact (`add` and `update` take email and permission, `rm` takes email, `ls` takes none; all take `--project`).

Method: documentation only; no commands were run.
