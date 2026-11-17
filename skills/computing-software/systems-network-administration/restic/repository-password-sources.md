---
id: computing-software.systems-network-administration.restic.repository-password-sources
name: repository-password-sources
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, password, password-file, password-command, automation, secrets]
level: practitioner
status: docs-checked
description: "Supply the restic repository location and password non-interactively using environment variables, files or a command, without leaking secrets to the process list."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
  - https://restic.readthedocs.io/en/stable/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Supply repository and password automatically

## Repository location

- `-r` / `--repo`
- `RESTIC_REPOSITORY`
- `--repository-file` or `RESTIC_REPOSITORY_FILE`

## Password

- `RESTIC_PASSWORD`
- `--password-file` or `RESTIC_PASSWORD_FILE`
- `--password-command` or `RESTIC_PASSWORD_COMMAND`

## Keep secrets out of the process list

The FAQ warns against inline assignment such as `RESTIC_PASSWORD=pw restic ...`, the `env` command and `system()` calls, because they can expose the password in the process list. Safer patterns:

- `export` the variable inside a script. Process environments are readable only by the same user.
- Use a password file with strict permissions, for example mode `0600` owned by root.
- Use `RESTIC_PASSWORD_COMMAND`. The command's output is read by restic, and the password itself never sits in the environment.

A macOS Keychain example from the FAQ:

```
export RESTIC_PASSWORD_COMMAND="security find-generic-password -a resticGCS -s restic_pwd -w"
```

The same approach can fetch `RESTIC_REPOSITORY` and cloud credentials.

## Choosing a password

Length is the single most important component of password strength; a strong password includes letters, digits and special characters. The FAQ names OpenSSL, pwgen and KeePass as tools that can generate one. Losing the password means the data is irrecoverably lost.

## Checked

2026-11-03. Confirmed in the restic docs pages Preparing a new repository (repository and password options) and FAQ (How can I specify encryption passwords automatically; How do I choose a strong password): option and variable names, the inline-assignment, `env` and `system()` warning, `export` in a script, `0600` file permissions, `RESTIC_PASSWORD_COMMAND`, the macOS Keychain example. Removed: the claim that flags override environment variables and the advice to keep a separate copy of the password (not in the docs).

Method: documentation only; no commands were run.
